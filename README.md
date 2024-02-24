# Datathon 2024 - AED Placement Optimization
*This is a group work of team Dplus for Datathon 2024 organized by Leuven Statistics Research Centre (LStat).
The original data for this work is from https://github.com/GregCollab/Datathon_2024.*

## Main idea for modelling
We optimized the geo-locations for AED placement in Flemish Brabant & Brussels regions
via solving a Maximal Coverage Location Optimization Problem, which is formulated as

$$
\begin{align}
    \textbf{Max}\quad &z = \sum_{i\in \mathcal{I}} w_i y_i\\
    \textbf{Subject to}\quad 
    & \sum_{j\in N_i} x_j \geq y_i \\
    & \sum_{j\in\mathcal{J}} x_j = K \\
    & x_j\in \{0,1\}, j\in \mathcal{J} \\
    & y_i\in \{0,1\}, i\in \mathcal{I} \\
    &N_i = \{j\in\mathcal{J}| d_{ij}\leq r\}
\end{align}
$$
, with some notations 

$$
\begin{align*}
    &\mathcal{I}: \text{Set of Cardiac Arrest type interventions}\\
    &\mathcal{J}: \text{Set of candidate AED sites}\\ 
    &r: \text{Maximal AED covered range (200 meters)} \\
    &x_j: \text{AED is allocated on the $j$th condidate site (1) or not (0)} \\
    &y_i: \text{The $i$th intervention is covered by at least one AED}\\ &\text{within radius $r$ (1) or not (0)}\\
    &K: \text{Number of AEDs to be selected} \\
    &w_i: \text{patient waiting time in $i$th intervention} \\
    &d_{ij}: \text{Haversine distance between the $i$th intervention and $j$th AED site}
\end{align*}
$$.

The objective is to maximize the number of cardiac arrest related cases "covered" within the appropriate distance to the nearest AED.
A weight (patient waiting time for ambulance) is assigned to each intervention case to prioritize the allocation of AEDs to areas where ambulance response time is too long.
