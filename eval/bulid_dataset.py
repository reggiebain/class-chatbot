from ls_utils.langsmith_utils import init_langsmith, load_prompt_from_langsmith, get_langsmith_client
from langsmith import traceable

def build_dataset():

    init_langsmith()
    client = get_langsmith_client()
    
    # Load pre made dataset from langsmith account
    dataset_name = 'class-chatbot-eval'
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"Successfully loaded dataset: {dataset.name} (ID: {dataset.id})")
    except Exception as e:
        print(f"Error: Dataset '{dataset_name}' not found or inaccessible. {e}")
        exit(1)

    # Print a few examples
    examples = list(client.list_examples(dataset_id=dataset.id))
    for example in examples:
        print(f"Question: {example.inputs['question']}")
        print(f"Answer: {example.outputs['answer']}")
        print("---")    
    # Create the dataset and examples in LangSmith
    #dataset_name = "physics1_syllabus_eval_dataset"
    #dataset = client.create_dataset(dataset_name=dataset_name)
    #client.create_examples(
    #    dataset_id=dataset.id,
    #    examples=examples
    #)

