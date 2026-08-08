# Statistical reporting

Record before execution:

- sampling unit: seed, rollout, subject, task, or example;
- number of independent units;
- aggregation function;
- uncertainty interval and calculation method;
- paired or unpaired comparison;
- missing, failed, and empty-output policy;
- multiple-comparison correction when relevant.

Do not use variation across examples as variation across independent training seeds. Do not convert one observed run into a multi-run success metric. Report the full denominator whenever failures or empty outputs are possible.
