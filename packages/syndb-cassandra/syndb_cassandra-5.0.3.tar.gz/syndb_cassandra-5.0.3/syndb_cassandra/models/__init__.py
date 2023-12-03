from cassandra.cqlengine.models import Model

from syndb_cassandra.models.axon_dendrite import dendrite_axon_models
from syndb_cassandra.models.neuron import Neuron
from syndb_cassandra.models.organelle import organelle_models
from syndb_cassandra.utils.misc import get_class_names, get_column_types
from syndb_constants.table import SyndbTable, table_name_to_syndb_table

structure_models: list[Model] = [Neuron, *dendrite_axon_models]
structure_model_names: list[str] = get_class_names(structure_models)

daughter_models: list[Model] = [*dendrite_axon_models, *organelle_models]

brain_unit_models: list[Model] = [Neuron, *daughter_models]
brain_unit_model_names: list[str] = get_class_names(brain_unit_models)

model_name_to_model: dict[str, Model] = dict(zip(brain_unit_model_names, brain_unit_models))

model_name_to_schema_dict: dict[str, dict[str, str]] = {
    n: get_column_types(model) for n, model in model_name_to_model.items()
}
syndb_table_to_schema_dict: dict[SyndbTable, dict[str, str]] = {
    table_name_to_syndb_table[n]: s for n, s in model_name_to_schema_dict.items()
}
