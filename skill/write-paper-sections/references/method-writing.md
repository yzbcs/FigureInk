# Method writing

## Section order

1. problem setup, notation, inputs, and outputs;
2. overview that matches the main method figure;
3. components in execution order;
4. training, inference, optimization, or search procedure;
5. complexity, implementation boundary, and reproducibility details.

## Component paragraph

For each component, write:

1. why the component is needed;
2. what it receives;
3. what operation it performs;
4. what it emits;
5. how the output is used downstream.

Do not report gains inside the method section. Do not use an equation when a named operation is clearer, and do not replace a necessary equation with vague prose.
