from typing import Type, Union
import json
from contextlib import contextmanager
from sqlalchemy.exc import ResourceClosedError

import pandas as pd

from sqlalchemy.orm import scoped_session

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, delete, update, text as sql_text

from sqlalchemy import create_engine
from .models import BasicResource, BasicWork, Precalculation, MSCHMModel
from .models import WorkModel, Unit, Edge, UnitType, Sign, Parameter, S7Model




class MschmAdapter:
    def __init__(self, url, echo=False):
        self.engine = create_engine(url, echo=echo)
        self.session_factory = sessionmaker(bind=self.engine)

        self.basic_objects_for_insert = {
            BasicWork: [],
            BasicResource: [],
            Unit: [],
        }

        self.works: list[BasicWork] = []
        self.resources: list[BasicResource] = []
        self.precalculations: list[Precalculation] = []


        self.basic_collections = {
            BasicWork: self.__get_basic_objects(BasicWork),
            BasicResource: self.__get_basic_objects(BasicResource),
            Unit: self.__get_basic_objects(Unit)
        }

    def save_precalculation_to_db(self, data: dict) -> None:
        for work_name, work_data in data.items():
            work = self.__handle_basic_name(BasicWork, work_name)
            self.delete_precalculation(work)
            self.__parse_work_data(work_data_dict=work_data, work=work)

        self.__save(self.basic_objects_for_insert.values())
        self.__save([self.precalculations])
        self.__update()

    def delete_precalculation(self, work):
        self.__execute_query(delete(Precalculation).where(Precalculation.id_basic_work == work.id), True)

    def save_model_to_db(self, model):
        models = []
        for k, v in model.items():
            self.delete_model(k)
        for work_name, work_data in model.items():
            work_model = WorkModel(
                    id=self.__get_last_id_from_db(WorkModel) + 1,
                    id_basic_work=self.__handle_basic_name(BasicWork, work_name).id,
            )
            models.append(work_model)
            types = [
                UnitType(
                    id=self.__get_last_id_from_db(UnitType)+n+1,
                    value=value,
                    id_model=work_model.id,
                    id_unit=self.__handle_basic_name(Unit, unit_name).id
                ) for n, (unit_name, value) in enumerate(work_data["info"]["types"].items())
            ]

            signs = [
                Sign(
                    id=self.__get_last_id_from_db(Sign) + n + 1,
                    value=value,
                    id_model=work_model.id,
                    id_unit=self.__handle_basic_name(Unit, unit_name).id
                ) for n, (unit_name, value) in enumerate(work_data["info"]["signs"].items())
            ]

            edges = [
                Edge(
                    id=self.__get_last_id_from_db(Edge) + n + 1,
                    id_model=work_model.id,
                    id_start=self.__handle_basic_name(Unit, v[0]).id,
                    id_finish=self.__handle_basic_name(Unit, v[1]).id,
                ) for n, v in enumerate(work_data["edges"])
            ]

            parameters = [
                Parameter(
                    id=self.__get_last_id_from_db(Parameter) + n + 1,
                    id_model=work_model.id,
                    id_unit=self.__handle_basic_name(Unit, unit_name).id,
                    mean=values["mean"],
                    regressor_obj=r'{}'.format(values["regressor_obj"]),
                    regressor=values["regressor"],
                    variance=values["variance"],
                    serialization=values["serialization"]
                ) for n, (unit_name, values) in enumerate(work_data["parameters"].items())
            ]

        self.__save(self.basic_objects_for_insert.values())
        self.__save([models, types, signs, edges, parameters])
        self.__update()


    def get_precalculation(self, name_of_works: list[str]) -> dict:
        result = {}
        self.__update()
        basic_resources_ids_dict = {o.id: o for o in self.basic_collections[BasicResource].values()}
        basic_works_ids_dict = {o.id: o for o in self.basic_collections[BasicWork].values() if o.name in name_of_works}

        precalculation_data = self.__execute_query(
            select(Precalculation
                   ).where(Precalculation.id_basic_work.in_(basic_works_ids_dict))
                   )

        if len(precalculation_data) == 0:
            raise ValueError(f"Works not found")

        df = pd.DataFrame([o.__dict__ for o in precalculation_data]).drop("_sa_instance_state", axis=1)
        df["basic_work_name"] = df["id_basic_work"].apply(lambda x: basic_works_ids_dict[x].name)
        df["basic_resource_name"] = df["id_basic_resource"].apply(lambda x: basic_resources_ids_dict[x].name)

        for row in df.to_dict(orient="records"):
            work_name = row["basic_work_name"]
            prob = row["work_value_probability"]
            work_value = row["work_value"]
            res_name = row["basic_resource_name"]
            res_value = row["res_value"]
            res_prob = f'{row["probability"]}%'

            if work_name not in result:
                result[work_name] = {}
            if work_value not in result[work_name]:
                result[work_name][work_value] = {}
            if res_prob not in result[work_name][work_value]:
                result[work_name][work_value][res_prob] = {}
            result[work_name][work_value][res_prob][res_name] = res_value
            result[work_name][work_value]["Prob"] = prob

        return result

    def get_models(self, name_of_works: list[str]):
        result = {}
        for work_name in name_of_works:
            try:
                work = self.__execute_query(select(BasicWork).where(BasicWork.name == work_name))
            except IndexError:
                work = None
            if work is None:
                continue
            if isinstance(work, list):
                if len(work) > 0:
                    work = work[0]
                else:
                    continue
            else:
                continue

            if work not in result:
                result[work_name] = {
                    "info": {
                        "types": {},
                        "signs": {},
                    },
                    "edges": [],
                    "parameters": {},
                }

            model = self.__execute_query(select(WorkModel).where(WorkModel.id_basic_work == work.id))
            if len(model):
                model = model[0]
            else:
                continue
            units = {o.id: o.name for o in self.__execute_query(select(Unit))}

            result[work_name]["info"]["types"] = {
                units[o.id_unit]: o.value for o in self.__execute_query(select(UnitType).where(
                                            UnitType.id_model == model.id,
                ))
            }

            result[work_name]["info"]["signs"] = {
                units[o.id_unit]: o.value for o in self.__execute_query(select(Sign).where(
                                            Sign.id_model == model.id,
                ))
            }

            result[work_name]["edges"] = [
                [units[o.id_start], units[o.id_finish]] for o in sorted(self.__execute_query(select(Edge).where(
                                            Edge.id_model == model.id
                )), key=lambda x: x.id)
            ]

            result[work_name]["parameters"] = {
                units[o.id_unit]: {
                    "mean": o.mean,
                    "regressor_obj": o.regressor_obj,
                    "regressor": o.regressor,
                    "variance": o.variance,
                    "serialization": o.serialization
                } for o in self.__execute_query(select(Parameter).where(
                    Parameter.id_model == model.id))
            }

        return result

    def delete_model(self, work_name):
        self.__update()
        try:
            work = self.basic_collections[BasicWork][work_name]
            model = self.__execute_query(select(WorkModel).where(WorkModel.id_basic_work==work.id))[0]

            self.__execute_query(delete(UnitType).where(
                                                UnitType.id_model == model.id,
            ), True)
            self.__execute_query(delete(Sign).where(
                                                Sign.id_model == model.id,
            ), True)
            self.__execute_query(delete(Sign).where(
                                                Sign.id_model == model.id,
            ), True)
            self.__execute_query(delete(Parameter).where(
                                                Parameter.id_model == model.id
            ), True)
            self.__execute_query(delete(WorkModel).where(
                                                WorkModel.id == model.id
            ), True)
        except KeyError:
            return
        except IndexError:
            return

    def save_s7_model(self, model):
        models_to_write = []
        for name, data in model.items():
            # check if model in database
            current = self.get_s7_model(name)
            if current is None:
                self.__execute_query(delete(S7Model).where(S7Model.name==name))
            data = json.dumps(data)
            models_to_write.append(S7Model(name=name,
                                           data=data))
        self.__save([models_to_write])

    def get_s7_model(self, name):
        result = self.__execute_query(select(S7Model).where(S7Model.name==name))
        if len(result) == 0:
            return
        else:
            return json.loads(result[0].data)

    def __update(self):
        self.precalculations = []
        self.resources = []
        self.basic_collections = {
            BasicWork: self.__get_basic_objects(BasicWork),
            BasicResource: self.__get_basic_objects(BasicResource),
            Unit: self.__get_basic_objects(Unit),
        }

    def __parse_work_data(self, work_data_dict: dict[str, dict], work: BasicWork):
        for work_value, prob_data in work_data_dict.items():
            work_value_prob = prob_data["Prob"]
            for probability, res_data in prob_data.items():
                if isinstance(res_data, dict):
                    for res_name, res_value in res_data.items():
                        resource = self.__handle_basic_name(BasicResource, res_name)

                        self.precalculations.append(
                            Precalculation(
                                id=self.__get_last_id(self.precalculations, Precalculation)+1,
                                id_basic_work=work.id,
                                id_basic_resource=resource.id,
                                work_value=float(work_value),
                                res_value=float(res_value),
                                probability=int(probability[:-1]),
                                work_value_probability=work_value_prob,
                            )
                        )

    def __handle_basic_name(self, basic_cls: Union[Type[BasicWork], Type[BasicResource]],
                            name: str) -> Union[BasicWork, Type]:
        collection = self.basic_collections[basic_cls]
        if name in collection:
            return collection[name]
        obj = basic_cls(
                        id=self.__get_last_id(list(collection.values()), basic_cls) + 1,
                        name=name
                )
        collection[name] = obj
        self.basic_objects_for_insert[basic_cls].append(obj)
        self.basic_collections[basic_cls][name] = obj
        return obj

    def __get_last_id_from_db(self, cls: Type[MSCHMModel]):
        query = sql_text(f"select max(id) from {cls.__tablename__}")
        last_id = self.__execute_query(query)
        last_id = last_id[0]
        if last_id is None:
            return 0
        return last_id

    def __get_basic_objects(self, cls):
        query = select(cls)
        result = self.__execute_query(query)
        return {o.name: o for o in result}

    def __save(self, collections: list[list]):
        for collection in collections:
            self.__save_to_database(collection)

    def __save_to_database(self, collection):
        with self.__get_session() as context:
            context.add_all(collection)
            context.commit()

    def __get_last_id(self, collection: list, cls: Type[MSCHMModel]):
        if len(collection):
            return max([o.id for o in collection])
        else:
            last_id = self.__get_last_id_from_db(cls)
            return 0 if last_id is None else last_id

    def __execute_query(self, query, commit=False):
        with self.__get_session() as context:
            result = context.execute(query)
            try:
                result = result.scalars().all()
            except ResourceClosedError:
                pass
            if commit:
                context.commit()

        return result

    @contextmanager
    def __get_session(self):
        session = scoped_session(self.session_factory)
        try:
            yield session
        finally:
            session.close()
