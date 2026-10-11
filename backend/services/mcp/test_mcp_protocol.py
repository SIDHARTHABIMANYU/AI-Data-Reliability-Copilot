
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.anyio
async def test_mcp_server_discovers_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.list_tools()
            tool_names = {tool.name for tool in result.tools}

            assert "pipeline_runs" in tool_names
            assert "data_quality_results" in tool_names
            assert "incident_records" in tool_names
            assert "anomaly_results" in tool_names
            assert "remediation_status" in tool_names



@pytest.mark.anyio
async def test_mcp_pipeline_tool_rejects_invalid_limit():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "pipeline_runs",
                arguments={"limit": 0},
            )

            # MCP should reject invalid arguments at the tool boundary.
            assert result.isError
            assert result.content
            assert "greater than or equal to 1" in result.content[0].text


@pytest.mark.anyio
async def test_mcp_quality_tool_rejects_invalid_limit():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "data_quality_results",
                arguments={"limit": 101},
            )

            assert result.isError
            assert result.content
            assert "less than or equal to 100" in result.content[0].text


@pytest.mark.anyio
async def test_pipeline_tool_rejects_empty_dataset_filter():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "pipeline_runs",
                arguments={"dataset": ""},
            )

            assert result.isError
            assert result.content
            assert "at least 1 character" in result.content[0].text


@pytest.mark.anyio
async def test_quality_tool_rejects_empty_status_filter():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "data_quality_results",
                arguments={"check_status": ""},
            )

            assert result.isError
            assert result.content
            assert "at least 1 character" in result.content[0].text
            

@pytest.mark.anyio
async def test_mcp_anomaly_tool_rejects_invalid_limit():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "anomaly_results",
                arguments={"limit": 101},
            )

            assert result.isError
            assert result.content
            assert "less than or equal to 100" in result.content[0].text


@pytest.mark.anyio
async def test_mcp_remediation_tool_rejects_invalid_id():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "backend.services.mcp.server"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "remediation_status",
                arguments={"remediation_id": 0},
            )

            assert result.isError
            assert result.content
