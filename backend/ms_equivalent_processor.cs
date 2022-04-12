// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");
using System.Text.RegularExpressions;


//Console.WriteLine(Example.testAnything().IsMatch("me@gmail.com"));


partial class Example

{
    private const string stringtotest = @"(aab)*"; // note that you need the @ symbol to the left of the " to escape the escape characters
    // old regex ^\S+@\S+$
   [RegexGenerator(stringtotest)]

    public static partial Regex testAnything();
    

}