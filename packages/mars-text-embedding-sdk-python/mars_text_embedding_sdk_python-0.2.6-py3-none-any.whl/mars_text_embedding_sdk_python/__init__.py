import numpy as np

from requests import post
from dataclasses import dataclass, fields
from operator import attrgetter
from typing import Optional, List, Dict, Callable
from pickle import loads
from gzip import decompress
from base64 import b64decode
from itertools import chain, starmap

@dataclass
class KeyValue:
        
    key:   str
    value: str
    
    def __eq__(self, other: 'KeyValue') -> bool:
        return self.key == other.key and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.key + str(self.value))

    def from_dict(d: dict) -> 'KeyValue':
        return KeyValue(
            key=d["key"],
            value=d["value"],
        )
    
    def from_tuple(t: tuple) -> 'KeyValue':
        return KeyValue(
            key=t[0],
            value=t[1],
        )
    
    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
        }
    
@dataclass
class Object:

    key_values: List[KeyValue]

    def __hash__(self) -> int:
        return hash(
            sorted(
                self.key_values,
                key=lambda x: x.key,
            )
        )
    
@dataclass
class Embedding:

    vector: np.ndarray
    key_value: KeyValue

    def __eq__(self, other: 'Embedding') -> bool:
        return np.array_equal(self.vector, other.vector) and self.key_value == other.key_value

@dataclass
class EmbeddingCollection:

    embeddings: List[Embedding]

    def to_array(self) -> np.ndarray:
        return np.array(
            list(
                map(
                    lambda x: x.vector,
                    self.embeddings
                )
            )
        )

@dataclass
class CoefPredicate:

    predicate: Callable[[KeyValue], bool]
    coefficient: float

    def __call__(self, embedding_component: Embedding) -> Embedding:
        if self.predicate(embedding_component.key_value):
            return Embedding(
                vector=embedding_component.vector*self.coefficient,
                key_value=embedding_component.key_value,
            )
        return embedding_component
    
@dataclass
class PredicateGroup:

    name: str
    predicate: Callable[[KeyValue], bool]

@dataclass
class GroupEmbedding:

    name: str
    embeddings: List[Embedding]

    def to_array(self, agg = lambda x: x) -> np.ndarray:
        return agg(
            np.array(
                list(
                    map(
                        lambda x: x.vector,
                        self.embeddings
                    )
                )
            )
        )
    
    def aggregate(self, agg = lambda x: x) -> Embedding:
        return Embedding(
            vector=self.to_array(agg=agg),
            key_value=KeyValue(key=self.name, value=""),
        )
    
    def aggregate_mean(self) -> Embedding:
        return self.aggregate(agg=lambda x: np.mean(x, axis=0))
    
    def aggregate_var(self) -> Embedding:
        return self.aggregate(agg=lambda x: np.var(x, axis=0))

@dataclass
class EmbeddingCollectionComposer:

    groups:     List[List[int]]
    embeddings: Dict[int, Embedding]

    def __repr__(self):
        nodef_f_repr = ", ".join(
            chain(
                map(
                    lambda f: f"{f.name}={attrgetter(f.name)(self)}",
                    filter(
                        lambda f: f.name != "embeddings",
                        fields(self)
                    )
                ),
                [
                    "embeddings={...}"
                ]
            )
        )
        return f"{self.__class__.__name__}({nodef_f_repr})"

    def __getitem__(self, key: int) -> List[Embedding]:
        return EmbeddingCollection(
            embeddings=list(
                map(
                    lambda x: self.embeddings[x],
                    self.groups[key]
                )
            )
        )
    
    def to_arrays(self, agg = lambda x: x) -> List[np.ndarray]:
        return list(
            map(
                lambda i: agg(self[i].to_array()),
                range(
                    len(self.groups)
                )
            )
        )
    
    def move_by_selector(self, selector: CoefPredicate) -> List[np.ndarray]:

        """
            Selects embeddings given `selector` predicate, average them into one vector (or taking the point if it is given) and subtracts it from all embeddings.
            The coefficient is "how much" to move the embeddings towards the selected embeddings. You can imagine all points moving 
            towards one specific point, where the coefficient is the "how much" to move.

            NOTE: If no vectors are selected, the embeddings are not moved.

            :param selector: A predicate to select embeddings.
            :return: ndarray. The moved embeddings as vectors and groups
        """
        target_mean_points = list(
            map(
                lambda group: np.array(
                    list(
                        map(
                            lambda i: self.embeddings[i].vector,
                            filter(
                                lambda i: selector.predicate(self.embeddings[i]),
                                group
                            )
                        )
                    ) or np.zeros_like(self.embeddings[0].vector),
                ).mean(axis=0),
                self.groups
            )
        )

        return list(
            starmap(
                lambda i, arr: (arr + target_mean_points[i]) * selector.coefficient if type(target_mean_points[i]) == np.ndarray else arr,
                starmap(
                    lambda i, group: (
                        i,
                        np.array(
                            list(
                                map(
                                    lambda idx: self.embeddings[idx].vector,
                                    group
                                )
                            )
                        ),
                    ),
                    enumerate(self.groups)
                )
            )
        )
    
    def group(self, predicate_groups: List[PredicateGroup], agg: Callable[[GroupEmbedding], Embedding] = lambda x: x) -> List[List[GroupEmbedding]]:

        """
            Groups embeddings by the predicate groups.
            If no match from predicate groups, the embedding is not included in the result.

            :param predicate_groups: A list of predicate groups.
            :return: A list of lists of group embeddings.
        """

        new_groups = []
        for group in self.groups:
            new_sub_groups = {}
            for embedding in group:
                for predicate_group in predicate_groups:
                    new_sub_groups.setdefault(predicate_group.name, [])
                    if predicate_group.predicate(self.embeddings[embedding].key_value):
                        new_sub_groups[predicate_group.name].append(self.embeddings[embedding])
            new_groups.append(
                list(
                    map(
                        lambda k: agg(
                            GroupEmbedding(
                                name=k,
                                embeddings=new_sub_groups[k],
                            ),
                        ),
                        new_sub_groups,
                    )
                )
            )

        return new_groups                

@dataclass
class Result:

    data:   Optional[EmbeddingCollectionComposer]   = None
    error:  Optional[str]                           = None

@dataclass
class EmbeddingSDK:
    
    url: str

    @staticmethod
    def _prepare_objects(key_values: List[KeyValue]) -> dict:

        """
            Returns a dictionary of unique key-value objects.
        """
        return 

    def __call__(self, objects: List[List[KeyValue]], dims: int = 300) -> Result:

        """
            Converts a list of key-value objects, into a list of embedding objects.

            :param objects: A list of lists of key-value objects to be converted into embeddings.
            :param dims: The number of dimensions of the embedding. Check API documentation for supported dimensions.
            :return: EmbeddingCollectionComposer.
        """

        try:
            object_dicts = dict(
                map(
                    lambda x: (hash(x), x),
                    chain(
                        *map(
                            lambda x: x.key_values, 
                            objects
                        )
                    ),
                )
            )
            response = post(
                self.url, 
                json={
                    "query": """
                        query VectorQuery($keyValues: [[KeyValueInput!]!]!) {
                            fromKeyValues(keyValues: $keyValues) {
                                asVectors(model: D"""+str(dims)+""") {
                                    vectors {
                                        compressed
                                    }
                                }
                            }
                        }
                    """,
                    "variables": {
                        "keyValues": [
                            list(
                                map(
                                    lambda x: x.to_dict(),
                                    object_dicts.values(),
                                )
                            )
                        ],
                    }
                }
            )

            if response.status_code == 200:
                if "errors" in response.json():
                    return Result(error=response.json()["errors"][0]["message"])
                
                return Result(
                    data=EmbeddingCollectionComposer(
                        groups=list(
                            map(
                                lambda xs: list(
                                    map(
                                        lambda y: hash(y),
                                        sorted(
                                            set(xs.key_values),
                                            key=xs.key_values.index,
                                        )
                                    )
                                ),
                                objects,
                            )
                        ),
                        embeddings=dict(
                            starmap(
                                lambda key, compressed_vector: (
                                    key,
                                    Embedding(
                                        vector=np.array(
                                            loads(
                                                decompress(
                                                    b64decode(
                                                        compressed_vector["compressed"]
                                                    )
                                                )
                                            )
                                        ),
                                        key_value=object_dicts[key],
                                    ),
                                ),
                                zip(
                                    object_dicts.keys(),
                                    response.json()["data"]["fromKeyValues"][0]['asVectors']['vectors'],
                                )
                            )
                        )
                    )
                )

        except Exception as e:
            return Result(error=str(e))
