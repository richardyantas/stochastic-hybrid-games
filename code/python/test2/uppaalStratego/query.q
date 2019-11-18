/*

*/
strategy Opt =minE (action) [<=maxTimeSim]: <> Controller.DONE

/*

*/
simulate 1 [<=maxTimeSim] {action} under Opt