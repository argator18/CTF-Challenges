using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using PhotoEditor.Models;

namespace PhotoEditor.Controllers;

public class BaseAPIController : ControllerBase
{
    public String GetUsername(Dictionary<String,String> env) {
        Process process = new Process();
        process.StartInfo.FileName = "bash";
        process.StartInfo.Arguments = "-c 'whoami'"; 
        
        foreach (var kv in env)
        {
            process.StartInfo.EnvironmentVariables[kv.Key] = kv.Value;
        }
        
        process.StartInfo.UseShellExecute = false;
        process.StartInfo.RedirectStandardOutput = true;
        process.StartInfo.RedirectStandardError = true;
        process.Start();
        string output = process.StandardOutput.ReadToEnd();
        Console.WriteLine(output);
        string err = process.StandardError.ReadToEnd();
        Console.WriteLine(err);
        process.WaitForExit();

        return output + err;
    }
}