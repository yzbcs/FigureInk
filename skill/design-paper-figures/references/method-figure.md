# Method main figure

## Purpose

Let a reader reconstruct the method's execution order, novelty, and interfaces.

## Pipeline template

1. inputs and observable state;
2. preprocessing or encoding;
3. focal mechanism;
4. intermediate representation or memory;
5. decision, output, or objective;
6. training, supervision, or feedback relation when applicable.

## Design rules

- Match subsection order unless a different order is essential for comprehension.
- Use the strongest visual weight for the novel mechanism, not for the largest module.
- Separate training-only and inference-time paths.
- Show repeated modules as one component with an iteration marker rather than duplicated boxes.
- Put equations only where the mathematical operation is the main message.
- Keep implementation detail out of the overview; move it to a component panel or caption.

## Caption contract

State the input, each stage, the focal mechanism, output, and any dashed or feedback relation.
