"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers
from typing import Optional
from tap_freshservice.client import FreshserviceStream

class AssetsStream(FreshserviceStream):
    name = "assets"
    path = "/assets?workspace_id=0"
    records_jsonpath="$.assets[*]"
    
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for the child streams.
        Refer to https://sdk.meltano.com/en/latest/parent_streams.html"""
        return {"display_id": record["display_id"],
                "asset_id": record["id"]
            }
    
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("display_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("asset_type_id", th.IntegerType),
        th.Property("impact", th.StringType),
        th.Property("usage_type", th.StringType),
        th.Property("asset_tag", th.StringType),
        th.Property("user_id", th.IntegerType),
        th.Property("department_id", th.IntegerType),
        th.Property("location_id", th.IntegerType),
        th.Property("agent_id", th.IntegerType),
        th.Property("group_id", th.IntegerType),
        th.Property("assigned_on", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("author_type", th.StringType),
        th.Property("end_of_life", th.DateTimeType),
        th.Property("discovery_enabled", th.BooleanType)
    ).to_dict()
