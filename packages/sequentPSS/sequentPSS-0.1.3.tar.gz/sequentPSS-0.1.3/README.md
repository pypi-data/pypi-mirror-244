# sequentPSS
sequential parameter space search method based on global sensitivity analysis


## License
sequentPSS / version 0.1.1
- install:

```python
!pip install sequentPSS
```

## Usage (using sample simulation in library)

### 1. Preprocessing

###### The SPS algorithm consists of preprocessing and sequential calibration stages, with validation being optional. In this study,<i> k </i> number of parameters are denoted as <i> X </i>, while <i> d </i> number of outcomes are denoted as <i> Y </i>. The mathematical representation is:

$$
X = \{X_1, X_2, \cdots X_i, \cdots, X_k\} \in \mathbb{R}^k
$$

$$
Y = \{Y_1, Y_2, \cdots Y_j, \cdots, Y_d\} \in \mathbb{R}^d
$$


###### Each parameter \( X \) takes a parameter value \( x \) in the parameter space.
    
    
#### 1.1 set parameter and hyperparameter


``` python
import sequentPSS as sqp

# set parameter spaces
x1_list = [1,2,3,4,5]
x2_list = [1,2,3,4,5]
x3_list = [1,2,3,4,5]

# set hyper parameters
M = 150
k = 3

# ---  run simulations for M(2k+2) times with random parameter values---
multi_simul_df = sqp.multiple_simple_simulation(x1_list, x2_list, x3_list, M, k) 

multi_simul_df.head()
```

![df result of simulation](/sequentPSS/screenshot/multi_simul_df.head().png)


###### Here's the DataFrame representing the simulation results with three parameters (x1, x2, x3) and three simulation outcomes (y1, y2, y3)


#### 1.2 determining rmse_sel for calibration

###### Algorithm 1. Preprocessing (1): Determining a Criterion for Calibration

<img src="/sequentPSS/screenshot/Algorithm1.png" alt="Preprocessing(1): determining a criterion for calibration" width="450"/>

###### In the preprocessing step, the criterion for calibration, RMSE<i><sub>sel</sub></i>, is determined as illustrated in Algorithm 1. During process (1), a parameter value x is randomly selected for each X<sub>i</sub> based on a uniform distribution. These values are then combined to compute RMSE<i><sub>tem</sub></i> in each iteration. This procedure continues until reaching M(2k+2) iterations, as outlined in equation 1.

###### RMSE, a widely-used metric for model calibration, is employed here to assess the discrepancy between simulated outcomes and observed data. The threshold RMSE<i><sub>sel</sub></i> is set for each Y<sub>j</sub> as the upper limit RMSE from any parameter combination. Users can adjust the leniency index μ to control the calibration rigor. For instance, with a μ value of 0.1, the lower 10% of all RMSE values become the RMSE<i><sub>sel</sub></i> criteria. Setting μ too low might lead to overfitting, while a higher value can introduce undue uncertainty.

``` python
# --- preprocessing 1: determining a criterion for calibration

O_list = [sqp.O1, sqp.O2, sqp.O3] # observed data to list -
u = 0.1
rmse_sel_df, multi_simul_df_rmse_sel = sqp.prep1_criterion(O_list, multi_simul_df, u, k)

# now, we have the rmse_sel for all O (observed data O1, O2, O3 corresponding to y1, y2, y3).
rmse_sel_df
```

![rmse_sel_df](/sequentPSS/screenshot/rmse_sel_df.png)


#### 1.3 sorting Y and X for calibration

###### Algorithm 2. preprocessing (2): sorting X and Y

<img src="/sequentPSS/screenshot/Algorithm2.png" alt="preprocessing (2): sorting X and Y" width="450"/>

###### Algorithm 2 details the procedure for ordering <i>j</i> and <i>i</i> before calibration. Utilizing simulations from Algorithm 1, data generated from X to Y are used in processes (2) and (3). 

###### In process (2), <i>c(Y<sub>j</sub>)</i> showcases the proportion of instances where <i>RMSE<sub>tem</sub></i> is smaller than <i>RMSE<sub>sel</sub></i> compared to all cases <i>n</i>. A prominent <i>c(Y<sub>j</sub>)</i> indicates a broad parameter space apt for calibration. Therefore, <i>j</i> is arranged in descending order of <i>c(Y<sub>j</sub>)</i> for subsequent calibration phases. 

###### In process (3), the first-order sensitivity index of each <i>X<sub>i</sub></i> in relation to <i>Y<sub>j</sub></i> (denoted as <i>S<sub>ji</sub></i>) is organized in descending order. This index gauges the extent to which <i>X<sub>i</sub></i> uniquely impacts <i>Y<sub>j</sub></i>. If <i>X<sub>i</sub></i> has a significantly low sensitivity index, it might not notably influence the outcome variance and can be skipped from calibration. Calibration begins by focusing on the most critical parameters based on their sensitivity indices.


```python

# --- preprocessing 2: sorting Y for calibration

y_seq_df = sqp.sorting_Y(multi_simul_df_rmse_sel)
y_seq_df

```

![y_seq_df](/sequentPSS/screenshot/y_seq_df.png)

```python

# --- preprocessing 3: sorting X based on sensitivity analysis for calibration
problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[1, 5],
               [1, 5],
               [1, 5]]
}

x_seq_df = sqp.sorting_X(problem, multi_simul_df_rmse_sel, GSA = 'RBD-FAST') # run GSA
x_seq_df

```
![x_seq_df](/sequentPSS/screenshot/x_seq_df.png)

###### Now we have rmse_sel, sorted y and sorted x, we can run sequential calibration.


### 2. sequential calibration

###### Algorithm 3. parameter space searching and calibration for each <i>y<sub>j</sub></i>

<img src="/sequentPSS/screenshot/Algorithm3.png" alt="parameter space searching and calibration for each Yj" width="450"/>

###### Figure 1. parameter space search and calibration process <i>y<sub>j</sub></i>
<img src="/sequentPSS/screenshot/Fig1.png" alt="parameter space search and calibration process" width="650"/>


###### Algorithm 3 details sequential calibration using the ordered Y and X values from Algorithm 2. In process (4), <i>γ</i> stores selected parameter combinations for each X. Initially, a fixed parameter <i>v</i> from <i>X<sub>1</sub></i> is chosen with random selections from other X sets excluding <i>X<sub>1</sub></i>. If the RMSE of the <i>γ</i> combination is under the <i>RMSE<sub>sel</sub></i> threshold, <i>γ</i> is added to C with its RMSE value recorded in R. This iterates M times.

###### Subsequently, parameter space of <i>X<sub>1</sub></i> is reduced by eliminating <i>v</i> if many combinations involving <i>v</i> don't meet the <i>RMSE<sub>sel</sub></i> threshold. If <i>v</i> occurrences in C is below <i>τ * M</i>, <i>v</i> is removed from <i>X<sub>1</sub></i>. τ, a user-defined tolerance index, dictates the parameter space reduction intensity. High τ values can lead to significant parameter space reduction and stringent calibration, while low values keep more of <i>v</i> in C, making space reduction inefficient. This process repeats for <i>X<sub>2</sub></i> using the already reduced <i>X<sub>1</sub></i> space. Ultimately, we get the condensed parameter space for the X sets, displayed in Figure 1. If additional Y outcomes exist, the loop reinitiates with the shrunk X parameter spaces.


###### Equation 1. uncertainty of the calibrated parameter combination <i>y<sub>j</sub></i>
<img src="/sequentPSS/screenshot/Equation1.png" alt="uncertainty of the calibrated parameter combination" width="450"/>

###### After completing sequential calibration for all <i>Y</i>, the refined parameter combinations are the final output. The Uncertainty index <i>U</i> aids in identifying the optimal parameter set, with lower indices indicating higher trustworthiness. Based on Equation 4, <i>R</i> encompasses all RMSE outcomes, while <i>C</i> captures only those RMSEs falling beneath <i>RMSE<sub>sel</sub></i>. The ratio of <i>C</i> to <i>R</i> illustrates the reliability of each parameter set. Deducting this ratio from 1 produces the uncertainty measure U. For instance, if a parameter set yields an acceptable RMSE in 7 out of 10 instances, there's a 70% confidence in that result, yielding an uncertainty of 0.3 for that combo.


#### 2.1 round 1: calibrate parameters with y1
```python
# -- now we need to run sequential calibration with the previous sequence of y and x (y1 -> y3 -> y2 / x3 -> x2 -> x1) --
# First round of y1: fix x3
x1_list = [1,2,3,4,5]
x2_list = [1,2,3,4,5]
x3_list = [1,2,3,4,5]

fix_x3_y1_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x3', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x3_list, result_df = seqCalibration(fix_x = 'x3', fix_y = 'y1', rmse_sel = 401.295316, simul_result_df = fix_x3_y1_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x3 parameter space:', x3_list)
```

```
reliability of 'x3' for 'y1' (1 - uncertainty degree):  {3: 0.59, 4: 0.91, 5: 1.0}
updated x3 parameter space: [3, 4, 5]
```

###### Sequential calibration is conducted in the order of sorted y and x values. The first step involves fixing <i>x<sub>3</sub></i> (and calibrate with <i>y<sub>1</sub></i>). The RMSE_sel value corresponding to <i>y<sub>1</sub></i> and its matching O1 values are used (401.295316), along with the tolerance index (t).

---

```python
# Second round of y1: fix x2

fix_x2_y1_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x2', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x2_list, result_df = seqCalibration(fix_x = 'x2', fix_y = 'y1', rmse_sel = 401.295316, simul_result_df = fix_x2_y1_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x2 parameter space:', x2_list)
```

```
reliability of 'x2' for 'y1' (1 - uncertainty degree):  {1: 0.93, 2: 0.88, 3: 0.79, 4: 0.79, 5: 0.58}
updated x2 parameter space: [1, 2, 3, 4, 5]
```
---

```python
# Third round of y1: fix x1

fix_x1_y1_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x1', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x1_list, result_df = seqCalibration(fix_x = 'x1', fix_y = 'y1', rmse_sel = 401.295316, simul_result_df = fix_x1_y1_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x1 parameter space:', x1_list)
```

```
reliability of 'x1' for 'y1' (1 - uncertainty degree):  {1: 0.726, 2: 0.869, 4: 0.909, 3: 0.85, 5: 0.729}
updated x1 parameter space: [1, 2, 3, 4, 5]
```

#### 2.2 round 2: calibrate parameters with y3

```python
# First round of y3: fix x3

fix_x3_y3_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x3', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x3_list, result_df = seqCalibration(fix_x = 'x3', fix_y = 'y3', rmse_sel = 3.176924, simul_result_df = fix_x3_y3_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x3 parameter space:', x3_list)
```

```
reliability of 'x3' for 'y3' (1 - uncertainty degree):  {4: 0.41, 5: 0.62}
updated x3 parameter space: [4, 5]
```

---
```python
# second round of y3: fix x2

fix_x2_y3_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x2', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x2_list, result_df = seqCalibration(fix_x = 'x2', fix_y = 'y3', rmse_sel = 3.176924, simul_result_df = fix_x2_y3_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x2 parameter space:', x2_list)
```

```
reliability of 'x2' for 'y3' (1 - uncertainty degree):  {1: 0.689, 5: 0.531, 4: 0.515, 3: 0.657, 2: 0.478}
updated x2 parameter space: [1, 2, 3, 4, 5]
```
---

```python
# second round of y3: fix x1

fix_x1_y3_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x1', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x1_list, result_df = seqCalibration(fix_x = 'x2', fix_y = 'y3', rmse_sel = 3.176924, simul_result_df = fix_x1_y3_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x1 parameter space:', x1_list)
```

```
reliability of 'x2' for 'y3' (1 - uncertainty degree):  {1: 0.67, 2: 0.43, 3: 0.68, 4: 0.65, 5: 0.56}
updated x1 parameter space: [1, 2, 3, 4, 5]
```

#### 2.3 round 3: calibrate parameters with y2

```python
# First round of y2: fix x3

fix_x3_y2_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x3', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x3_list, result_df = seqCalibration(fix_x = 'x3', fix_y = 'y2', rmse_sel = 50.487752, simul_result_df = fix_x3_y2_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x3 parameter space:', x3_list)
```

```
reliability of 'x3' for 'y2' (1 - uncertainty degree):  {5: 0.678, 4: 0.429}
updated x3 parameter space: [4, 5]
```
---

```python
# second round of y2: fix x2

fix_x2_y2_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x2', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x2_list, result_df = seqCalibration(fix_x = 'x2', fix_y = 'y2', rmse_sel = 50.487752, simul_result_df = fix_x2_y2_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x2 parameter space:', x2_list)
```

```
reliability of 'x2' for 'y2' (1 - uncertainty degree):  {3: 0.25, 1: 0.421, 4: 0.396, 2: 0.333}
updated x2 parameter space: [1, 2, 3, 4]
```

---
```python
# second round of y2: fix x1

fix_x1_y2_simul_result_df = fix_param_simple_simulation(x1_list, x2_list, x3_list, fix_x = 'x1', M = 100) # fix x3: fix each x3 value one by one and run 100 times of simulation

x1_list, result_df = seqCalibration(fix_x = 'x1', fix_y = 'y2', rmse_sel = 50.487752, simul_result_df = fix_x1_y2_simul_result_df,  O_list = O_list, t = 0.2, df_return = True)

print('updated x1 parameter space:', x1_list)
```

```
reliability of 'x1' for 'y2' (1 - uncertainty degree):  {3: 0.443, 1: 0.34, 2: 0.634, 4: 0.541}
updated x1 parameter space: [1, 2, 3, 4]
```

---

The calibration results are as follows:
1. Calibration based on y1 in round 1 led to the following outcomes:

- x1: [1,2,3,4,5] -> [3,4,5]
- x2: [1,2,3,4,5] -> [1,2,3,4,5]
- x3: [1,2,3,4,5] -> [1,2,3,4,5]

2. Calibration based on y3 in round 2 led to the following outcomes:

- x1: [3,4,5] -> [4,5]
- x2: [1,2,3,4,5] -> [1,2,3,4,5]
- x3: [1,2,3,4,5] -> [1,2,3,4,5]

3. Calibration based on y2 in round 3 led to the following outcomes:

- x1: [4,5] -> [4,5]
- x2: [1,2,3,4,5] -> [1,2,3,4]
- x3: [1,2,3,4,5] -> [1,2,3,4]


---

## Related Document: 
 will be added

## Author

- **Author:** Moongi Choi
- **Email:** u1316663@utah.edu
