# Constrained Residual Race: An Efficient Hybrid Controller for Autonomous Racing
Deep reinforcement learning (DRL) has shown promise in solving the autonomous racing problem without requiring an accurate dynamics model, 
but random sampling of actions can lead to inefficient exploration. 
This paper proposes an efficient racing method, Constrained Residual Race (CRR), which combines a geometry-based reactive obstacle avoidance algorithm, 
Follow-The-Gap Method (FTG), with DRL. CRR generates safe guided actions with FTG and complementary actions with DRL, 
which are then fused into a final control action through a constraint equation. 
Using FTG as a prior controller enhances exploration efficiency and produces safe driving actions. 
Constraining the DRL policy output ensures that it does not overwrite the prior policy during early stages of exploration. 
Additionally, the DRL policy improves over the performance of the prior controller during training, reducing the lap time of the car. 
Validation on the F1TENTH simulator shows that CRR achieves lower lap times in most cases and exhibits excellent generalization capability.

## Demos
The results of our method on the four tracks, in order Austria, Berlin, Columbia and Treitlstrasse.

<img src="gif/Aus.gif" width="245"> <img src="gif/Ber.gif" width="245"> <img src="gif/Col.gif" width="245">

 <img src="gif/Tre.gif" width="745" height="245">



## Installation
Our code has been tested on `Ubuntu 20.04` with `Python 3.7` and `Tensorflow 2.3.0`. 

This F1TENTH simulator used the repository [racecar_gym](https://github.com/axelbr/racecar_gym).

DRL algorithm is based on [OpenAISpinningUp](https://github.com/openai/spinningup)
```
git clone https://github.com/openai/spinningup.git 
cd spinningup 
pip install -e . 
git clone https://github.com/axelbr/racecar_gym.git
cd racecar_gym
pip install -e .
pip install tensorflow==2.3.0 

```

To implement our setup in the experiment, 
please use file ```racecar.yml``` to replace 
```racecar.yml``` in 
```racecar_gym/models/vehicles/racecar/racecar.yml```.

## Training

By running file ```CRR.py``` for agent training, 
it is possible to change the track parameter in file ```CRR.py``` to achieve training on other tracks.

```
python CRR.py
```

## Acknowledgment

We use the following code in our project

* [ResRace](https://github.com/kaixindelele/ResRace)
* [SpinningUp](https://github.com/openai/spinningup)
* [Racecar_gym](https://github.com/axelbr/racecar_gym)
