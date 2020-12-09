//This file was generated from (Academic) UPPAAL 4.1.20-stratego-3 (rev. 6), August 2016

/*

*/
strategy Opt = minE (C) [<=timeHorizon]: <> y >= timeHorizon

/*

*/
simulate 1 [<=timeHorizon] {curr_speed} under Opt
