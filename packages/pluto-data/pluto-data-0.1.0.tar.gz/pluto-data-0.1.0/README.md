<div align="center">
    <h3 align="center">🌳 Oak: High-Quality Synthetic Data for LLM Fine-Tuning 🌳</h3><p></p>
    <img align="center" src="https://raw.githubusercontent.com/havenhq/oak/main/images/oak.png" height="300" alt="Oak" />
</div>

<div align="center">


<br>
<br>

[🌐 Website](https://haven.run/)
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
[💬 Discord](https://discord.gg/JDjbfp6q2G)
<br>

</div>


## Welcome 💚

Oak makes it easy to generate synthetic data for fine-tuning LLMs. Here's what you can do with it:

- Overcome repetitiveness and make your data highly diverse using topic trees
- Run multiple sampling requests in parallel to speed up data generation
- Use any model provider to generate data


## Quickstart 🚀

To get started, let's generate a dataset of coding questions about numpy. First install the oak library:

```
pip install oak-data
```

Then run the following code:

```python
from oak import EngineArguments, DataEngine, Dataset, TopicTree, TopicTreeArguments

system_prompt = "You are a helpful AI coding assistant. You help software developers with their coding questions and write code for them. You do not just give high level coding advice, but instead, you tend to respond to coding questions with specific code examples."

tree = TopicTree(
    args=TopicTreeArguments(
        root_prompt="Functionalities of numpy",
        model_system_prompt=system_prompt,
        tree_degree=10,
        tree_depth=2
    )
)

tree.build_tree(model_name="gpt-3.5-turbo-1106")
tree.save("numpy_topictree.jsonl")

engine = DataEngine(
    args=EngineArguments(
        instructions="Please specifically provide training examples with questions about numpy. A training sample should consist of just one question and a response, and not a chat with multiple messages.",
        system_prompt=system_prompt,
    )
)

dataset = engine.create_data(
    model_name="gpt-4-1106-preview",
    num_steps=20,
    batch_size=5,
    topic_tree=tree
)

dataset.save("output_with_topictree.jsonl")

```
