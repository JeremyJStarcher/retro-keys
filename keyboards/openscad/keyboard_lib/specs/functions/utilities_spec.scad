// openspecad --only-functions
use <../../lib/utilities.scad>

// Test reverse
assert(reverse(["c","b","a"]) == ["a","b","c"], "Reversed list did not match expected result");
assert(reverse(["a"]) == ["a"], "Reverse failed on single element array");
assert(reverse([]) == [], "Reverse failed on empty array");
echo("Reverse successful!");

// Test pop
assert(pop(["a","b","c"]) == ["b","c"], "Pop of list did not remove the expected element");
assert(pop(["a"]) == [], "Pop failed on single element array");
assert(pop([]) == [], "Pop failed on empty array");
echo("Pop successful!");
