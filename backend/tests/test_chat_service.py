import pytest

from app.core.exceptions import LLMProviderError
from app.core.models import Message
from app.services.chat_service import ChatService
from tests.fakes import FailingLLMProvider, RecordingLLMProvider


def test_new_session_gets_generated_id(chat_service):
    result = chat_service.chat("hello")

    assert result.session_id
    assert result.reply == "[fake] You said: hello"


def test_existing_session_id_is_kept(chat_service):
    result = chat_service.chat("hello", session_id="abc")

    assert result.session_id == "abc"


def test_user_and_assistant_messages_are_saved(chat_service, repository):
    result = chat_service.chat("hello")

    history = repository.get_history(result.session_id)
    assert [m.role for m in history] == ["user", "assistant"]


def test_previous_history_is_sent_to_llm(repository):
    llm = RecordingLLMProvider(reply="ok")
    service = ChatService(llm=llm, repository=repository)

    service.chat("first", session_id="s1")
    service.chat("second", session_id="s1")

    sent = llm.calls[-1]
    assert [m.content for m in sent] == ["first", "ok", "second"]


def test_conversation_sent_to_llm_starts_with_user(repository):
    repository.save_message("s1", Message("assistant", "orphan reply"))
    llm = RecordingLLMProvider()

    ChatService(llm=llm, repository=repository).chat("hi", session_id="s1")

    assert llm.calls[0][0].role == "user"


def test_nothing_is_saved_when_llm_fails(repository):
    service = ChatService(llm=FailingLLMProvider(), repository=repository)

    with pytest.raises(LLMProviderError):
        service.chat("hi", session_id="s1")

    assert repository.get_history("s1") == []