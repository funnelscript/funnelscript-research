"""Independent Phase 007G grammar and hand-calculated event oracle checks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_grammar_is_closed_for_new_expression_and_module_nonterminals():
    grammar = (ROOT / 'spec/grammar.ebnf').read_text()
    assert 'WorldImport           ::= "import" StringLiteral' in grammar
    assert 'NamedImport           ::= Identifier ("as" Identifier)?' in grammar
    assert 'AdditiveExpression    ::= MultiplicativeExpression' in grammar
    assert 'MultiplicativeExpression ::= PrimaryExpression' in grammar
    assert 'PrimaryExpression     ::= StateLiteral | PayloadReference | Identifier' in grammar
    assert 'BinaryRight           ::=' not in grammar
    spec = (ROOT / 'spec/phase-007g-composable-language-v1.md').read_text()
    for name in ('H-EXPR', 'H-MODULE', 'H-PLAYBOOK', 'snapshot', '1 MiB', '10,000'):
        assert name in spec


def test_oracle_is_independent_of_production_engine():
    receipt = json.loads((ROOT / 'evals/phase-007g-reference.json').read_text())
    assert receipt['schema'] == 'funnelscript-phase-007g-independent-example-v1'
    assert receipt['seed'] == 42
    assert {event['name'] for event in receipt['inputs']} == {'Balance.Tick', 'Lead.Tick'}
    initial_balance, initial_visits = 1, 0
    assert receipt['expected']['state']['Balance']['count'] == (initial_balance + 2) * 3
    assert receipt['expected']['state']['Lead']['visits'] == initial_visits + 3 * 2
    assert receipt['expected']['processed_events'] == 2
