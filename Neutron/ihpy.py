import inspect

"""
In-Html-Python

Example usage:
{python
         # The return statement works as in a function except that the return(s) get added to the HTML, works with strings, lists, and tuples.
         
         return "This will be displayed in the HTML", Neutron.elements.H2(win, content="This too")

}

"""
def compile(html, locals):
    
    if html.find("{python") != -1: # If it exists
        
        user_code = html[html.find("{python") + len("{python"):html.find("}")]

        runner_src = "def runner():\n" + user_code # To prevent any IndentationErrors and make the return statement work

        exec(runner_src, locals) # Define function
        result = eval("runner()", locals)

        in_python_html = html[html.find("{python"):html.find("}") + 1]

        if type(result) == tuple or type(result) == list:
           results_to_str = [str(i) for i in result]
           results_combined = "\n".join(results_to_str)
        
           return html.replace(in_python_html, results_combined)
        
        else:
           return html.replace(in_python_html, str(result))
    else:

        return html
