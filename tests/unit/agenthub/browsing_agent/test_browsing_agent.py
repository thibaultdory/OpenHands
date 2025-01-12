from unittest.mock import MagicMock

from openhands.agenthub.browsing_agent.browsing_agent import (
    BrowsingAgent,
    has_modal_dialog,
)
from openhands.core.config import AgentConfig


def test_has_modal_dialog():
    # Test with modal dialog present
    axtree_txt = """
    RootWebArea 'Google', focused
    [346] dialog 'Cookie Consent', clickable, modal=True
    [489] button 'Accept All', clickable
    """
    assert has_modal_dialog(axtree_txt) is True

    # Test without modal dialog
    axtree_txt = """
    RootWebArea 'Google', focused
    [99] combobox 'Search', clickable
    [260] button 'Google Search', clickable
    """
    assert has_modal_dialog(axtree_txt) is False


def test_browsing_agent_modal_dialog_handling():
    # Create a mock LLM
    mock_llm = MagicMock()
    mock_llm.format_messages_for_llm.return_value = []
    mock_llm.completion.return_value = {
        'choices': [{'message': {'content': 'click("489")'}}]
    }

    # Create a BrowsingAgent instance
    agent = BrowsingAgent(mock_llm, AgentConfig())

    # Import the module-level functions
    from openhands.agenthub.browsing_agent.browsing_agent import get_system_message, get_prompt

    # Verify that the system message includes modal dialog handling instructions
    system_msg = get_system_message('test goal', 'test action space')
    assert 'modal dialog' in system_msg
    assert 'cookie banner' in system_msg
    assert 'Accept All' in system_msg

    # Verify that the prompt includes modal dialog example
    prompt = get_prompt('', 'https://example.com', 'test tree', '')
    assert 'modal dialog' in prompt
    assert 'cookie consent' in prompt
    assert 'Accept All' in prompt