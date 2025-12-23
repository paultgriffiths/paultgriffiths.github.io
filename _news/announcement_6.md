---
date: "2025-10-31 08:59:00-4:00"
inline: false
layout: post
related_posts: false
title: VESRI model calibration workshop
description: Challenges of climate model calibration
---

Flying trip to an eerily quiet Washington DC, hosting a very lively Schmidt Sciences Virtual Earth System Research Institute meeting on model calibration. 

---

I would summarise the key challenges as

1. **Prohibitive Computational Cost:** This is a central and recurring bottleneck.
    - Running high-resolution, fully coupled ESMs requires immense computing power, limiting the number and length of simulations possible.
    - Specific model components, particularly those dealing with atmospheric chemistry (like ozone and methane reactions) and aerosol microphysics (including aerosol-cloud interactions), are computationally very expensive.
    - Simulating long timescales, necessary for "spinning up" slow components (like deep ocean circulation or ice sheets) or running paleo-climate transient simulations, is often computationally infeasible with complex models.
    - The cost restricts the ability to run large ensembles, which are crucial for quantifying uncertainty and performing robust model calibration.
    - Coupling "fast" components (atmosphere) with "slow" components (ice sheets, deep ocean carbon) efficiently is difficult, often leading to model drift or the need to use simplified, non-interactive components (like prescribed ice sheets).
        
2. **Uncertainty and Complexity in Process Representation:** Accurately representing key physical and chemical processes within the model grid is a major hurdle.
    - Many critical processes, especially aerosol-cloud interactions, occur at scales much smaller than typical ESM grid boxes and must be simplified through parameterizations, introducing significant uncertainty. Some processes just have no known data to underpin them, e.g. liquid water droplet coalescences as function of size and relative velocity. 
    - The climate system involves complex, non-linear interactions and feedbacks (e.g., chemistry-aerosol-cloud interactions, climate state-dependent feedbacks) that are difficult to fully capture in models. For example, the strength of feedbacks can change depending on the background climate state (like glacial vs. interglacial).
    - Solving the "stiff" systems of equations required for atmospheric chemistry is a known computational bottleneck.

<img src="https://www.instagram.com/paultgriffiths/p/DQfdjpfDNlj/" alt="post meeting walk">
