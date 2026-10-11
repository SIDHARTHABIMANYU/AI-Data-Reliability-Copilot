from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field, StringConstraints

from backend.services.mcp.tools import (
    get_pipeline_runs,
    get_data_quality_results,
    get_incidents,
    get_anomaly_results,
    get_remediation_status,
)


mcp = FastMCP("AI Data Reliability Copilot")


Limit = Annotated[int, Field(ge=1, le=100)]

FilterText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]


@mcp.tool()
def pipeline_runs(
    dataset: FilterText | None = None,
    limit: Limit = 20,
) -> dict:
    """Retrieve recent pipeline runs, optionally filtered by dataset."""
    return get_pipeline_runs(dataset=dataset, limit=limit)


@mcp.tool()
def data_quality_results(
    dataset: FilterText | None = None,
    check_status: FilterText | None = None,
    limit: Limit = 20,
) -> dict:
    """Retrieve data-quality results with optional filters."""
    return get_data_quality_results(
        dataset=dataset,
        check_status=check_status,
        limit=limit,
    )


@mcp.tool()
def incident_records(
    dataset: FilterText | None = None,
    status: FilterText | None = None,
    severity: FilterText | None = None,
    limit: Limit = 20,
) -> dict:
    """Retrieve incidents with optional dataset, status, and severity filters."""
    return get_incidents(
        dataset=dataset,
        status=status,
        severity=severity,
        limit=limit,
    )


@mcp.tool()
def anomaly_results(
    store_id: FilterText | None = None,
    anomaly_status: FilterText | None = None,
    limit: Limit = 20,
) -> dict:
    """Retrieve anomaly results with optional filters."""
    return get_anomaly_results(
        store_id=store_id,
        anomaly_status=anomaly_status,
        limit=limit,
    )


@mcp.tool()
def remediation_status(
    remediation_id: Annotated[int, Field(ge=1)],
) -> dict:
    """Read remediation status without approving, rejecting, or executing changes."""
    return get_remediation_status(remediation_id=remediation_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
