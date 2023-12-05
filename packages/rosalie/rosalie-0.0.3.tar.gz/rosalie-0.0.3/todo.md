
# todo
- [x] Very simple end-to-end process worke mechanically
- [x] Turn evaluation logic into a Class
- [x] Move Evaluator class to module
- [x] Multiple evaluators
    - [x] Primitive example
    - [x] Sensible defaults
    - [x] Pass no evaluator (use default)
    - [x] Pass one evaluator (compare to default)
    - [x] Pass two evaluators (compare to each other)
- [x] Multiple preprocessors
    - [x] Single preprocessor [x] Two preprocessors
    - [x] Three preprocessors
    - [x] Create a CUPED example
- [x] Simplify data passing
    - [x] Move aggregation out of class
    - [x] Simpler sample data creation process

CUPED example (mvp branch)
- [x] Understand current Causal JET cuped implementation
- [x] Get cuped evaluator to work in nb
- [x] Make cuped evaluator return p-value only
- [x] Pass dataframes, not arrays, to callables
- [x] Pass CJ cuped to evaluator
- [x] Clean up example
- [x] Complare CJ and traditional CUPED
- [x] Simpler dummy data
- [x] Cleanup
- [x] Support sampling time-series
- [x] Use OneDag data
- [x] Add tqdm
- [x] Run small evaluation to test process
- [x] Profile callables (CJ implementation seems very slow)
- [x] Separate preprocessing and evaluation for better performance
- [x] Fix issue with both evaluators having exact same results
    - The issue was that both the cuped evaluator and the plain wls one produced exactly the same results.
    - The solution was interesting: it happened because I first defined the cuped evaluator, so this one would run first, and because the cuped evaluator over-wrote the metric value with the adjusted metric value in the original dataset, which was then used by the plain wls, leading wls to also use the cuped-adjusted metric value.
- [x] Understand why cuped and quasi cuped delivered identical results (they didn't -- they produced slightly different results, just as expected given that they are effectively identical).
- [x] Handle all relevant data types -- customer, restaurant, city
    - [x] For restaurant and city, use pooled ols with clustered errors as we presently do in cj.

- [x] Turn into simple package for use in VR discovery.
- [x] Results object that can show data and produce graphs
- [ ] Add dataset to library

- [ ] Elegant solution to decorator registration (so list gets refreshed)
- [ ] Move info on evaluated functions into Evaluator


- [ ] Tool components
    - [ ] Engine
    - [ ] Library of evaluators
    - [ ] Library of datasets
    - [ ] Library of preprocessors (e.g. pre-experiment data)
    - [ ] Example notebook to show workflow
    - [ ] Visualisation tools



    

- [ ] Check Python resources for building such a tool best practices.
- [ ] Think about how to evaluate restaurant-level experiments (using pooled OLS with clustered std errors is incorrect!)
- [ ] Think about how to handle preprocessor -- pair with evaluator?
- [ ] Handle null values -- currently dropping them during pre data creation
- [ ] Support multiple MDES
- [ ] Translate sample size to experiment duration
- [ ] Use OneDag data for each unit of aggregation -- deprecated? Talk to Ciaran
- [ ] Improve notebook inteface
- [ ] Update instructions
- [ ] Improve speed of simulation -- parallalise? 
- [ ] Allow evaluators to return KPIs other than just p-value

- [ ] Cosmetics
    - [x] Consistent object naming
    - [ ] Custom labels
    - [ ] Beautify figure

