# Deep Play-by-Play

This repo contains model and data collection / preprocessing code to label NBA broadcast footage with play-by-play descriptions, using 3D ConvNet-based video classification.


### Classification performance
On a test set with 253 test examples (more or less evenly divided among 6 classes), the following accuracies were achieved:

| # classes        | Classes           | Accuracy  |
| ------------- |:-------------| :-----|
| 6      | (Inside/Midrange/Three) (Make/Miss) | 66% |
| 4      | (Two/Three) (Make/Miss)      | 74% |
| 2 | (Make/Miss)      | 91% |


### Examples:
The ultimate goal is continuous video classification, on running broadcast footage. However, I didn't have access to labelled data for non-field goal events (like free throws, rebounds, fouls, players running in transition). As a result, these examples use 90-frame videos of field-goal make/miss events - the only kind the model can currently identify.

<img src="missed_threes.gif" width="45%"> <img src="assets/PROBS_1.png" width="50%">
<img src="assets/PLAY_2.gif" width="45%"> <img src="assets/PROBS_2.png" width="50%">
<img src="assets/PLAY_4.gif" width="45%"> <img src="assets/PROBS_4.png" width="50%">
<img src="assets/PLAY_5.gif" width="45%"> <img src="assets/PROBS_5.png" width="50%">

### Incorrect classifications:
This Danny Green and-one is best classified as an `INSIDE_MAKE`, but `MIDRANGE_MAKE` is not a terribly bad guess:
<img src="assets/PLAY_7.gif" width="45%"> <img src="assets/PROBS_7.png" width="50%">


The following play is an offensive foul followed by a `MIDRANGE_MISS`, but is classified as more likely to be an `INSIDE_MAKE` (51%) than a `MIDRANGE_MISS` (27%):

<img src="assets/PLAY_6.gif" width="45%"> <img src="assets/PROBS_6.png" width="50%">


Sometimes, the classifier flat-out fails confidently:

<img src="assets/PLAY_3.gif" width="45%"> <img src="assets/PROBS_3.png" width="50%">
<img src="assets/PLAY_FAIL.gif" width="45%"> <img src="assets/PROBS_FAIL.png" width="50%">


