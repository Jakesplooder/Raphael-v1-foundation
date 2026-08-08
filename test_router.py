import sys
sys.path.insert(0, 'C:/RaphaelOS')
import voice_gateway

voice_config = voice_gateway.load_voice_config()

queries = [
    'world-model-query "Financial Council tasks"',
    'what tasks does the financial council have',
    'what is blocking the POD workflow'
]

for q in queries:
    res = voice_gateway.route_intent(q, voice_config)
    print(f'QUERY: {q}')
    print(f'INTENT: {res.intent}, COMMAND: {res.command}')
    print('-' * 40)
