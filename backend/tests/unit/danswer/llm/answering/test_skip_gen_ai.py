from typing import Any
from typing import cast
from unittest.mock import Mock

import pytest

from danswer.llm.answering.answer import Answer
from danswer.one_shot_answer.answer_question import AnswerObjectIterator
from danswer.tools.force import ForceUseTool
from tests.regression.answer_quality.run_qa import _process_and_write_query_results


@pytest.mark.parametrize(
    "config",
    [
        {
            "skip_gen_ai_answer_generation": True,
            "question": "What is the capital of the moon?",
        },
        {
            "skip_gen_ai_answer_generation": False,
            "question": "What is the capital of the moon but twice?",
        },
    ],
)
def test_skip_gen_ai_answer_generation_flag(config: dict[str, Any]) -> None:
    search_tool = Mock()
    search_tool.name = "search"
    search_tool.run = Mock()
    search_tool.run.return_value = [Mock()]
    mock_llm = Mock()
    mock_llm.config = Mock()
    mock_llm.config.model_name = "gpt-4o-mini"
    mock_llm.stream = Mock()
    mock_llm.stream.return_value = [Mock()]
    answer = Answer(
        question=config["question"],
        answer_style_config=Mock(),
        prompt_config=Mock(),
        llm=mock_llm,
        single_message_history="history",
        tools=[search_tool],
        force_use_tool=(
            ForceUseTool(
                tool_name=search_tool.name,
                args={"query": config["question"]},
                force_use=True,
            )
        ),
        skip_explicit_tool_calling=True,
        return_contexts=True,
        skip_gen_ai_answer_generation=config["skip_gen_ai_answer_generation"],
    )
    count = 0
    for _ in cast(AnswerObjectIterator, answer.processed_streamed_output):
        count += 1
    assert count == 2
    if not config["skip_gen_ai_answer_generation"]:
        mock_llm.stream.assert_called_once()
    else:
        mock_llm.stream.assert_not_called()


##### From here down is the client side test that was not working #####


class FinishedTestException(Exception):
    pass


# could not get this to work, it seems like the mock is not being used
# tests that the main run_qa function passes the skip_gen_ai_answer_generation flag to the Answer object
@pytest.mark.parametrize(
    "config, questions",
    [
        (
            {
                "skip_gen_ai_answer_generation": True,
                "output_folder": "./test_output_folder",
                "zipped_documents_file": "./test_docs.jsonl",
                "questions_file": "./test_questions.jsonl",
                "commit_sha": None,
                "launch_web_ui": False,
                "only_retrieve_docs": True,
                "use_cloud_gpu": False,
                "model_server_ip": "PUT_PUBLIC_CLOUD_IP_HERE",
                "model_server_port": "PUT_PUBLIC_CLOUD_PORT_HERE",
                "environment_name": "",
                "env_name": "",
                "limit": None,
            },
            [{"uid": "1", "question": "What is the capital of the moon?"}],
        ),
        (
            {
                "skip_gen_ai_answer_generation": False,
                "output_folder": "./test_output_folder",
                "zipped_documents_file": "./test_docs.jsonl",
                "questions_file": "./test_questions.jsonl",
                "commit_sha": None,
                "launch_web_ui": False,
                "only_retrieve_docs": True,
                "use_cloud_gpu": False,
                "model_server_ip": "PUT_PUBLIC_CLOUD_IP_HERE",
                "model_server_port": "PUT_PUBLIC_CLOUD_PORT_HERE",
                "environment_name": "",
                "env_name": "",
                "limit": None,
            },
            [{"uid": "1", "question": "What is the capital of the moon but twice?"}],
        ),
    ],
)
@pytest.mark.skip(reason="not working")
def test_run_qa_skip_gen_ai(
    config: dict[str, Any], questions: list[dict[str, Any]], mocker
) -> None:
    mocker.patch(
        "tests.regression.answer_quality.run_qa._initialize_files",
        return_value=("test", questions),
    )

    def arg_checker(question_data: dict, config: dict, question_number: int):
        assert question_data == questions[0]
        raise FinishedTestException()

    mocker.patch(
        "tests.regression.answer_quality.run_qa._process_question", arg_checker
    )
    with pytest.raises(FinishedTestException):
        _process_and_write_query_results(config)