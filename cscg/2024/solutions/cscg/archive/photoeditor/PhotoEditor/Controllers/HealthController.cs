using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using PhotoEditor.Models;

namespace PhotoEditor.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : BaseAPIController
{
    private readonly ILogger<DynamicPhotoEditorController> _logger;

    public HealthController(ILogger<DynamicPhotoEditorController> logger)
    {
        _logger = logger;
    }


    [HttpGet]
    [Route("Version")]
    public IActionResult Version()
    {
        return Content("{'Version':'1.0.0'}");
    }

    [HttpGet]
    [Route("User")]
    public IActionResult GetUser()
    {
        var username = GetUsername(new Dictionary<String,String> { { "PATH", "/usr/bin/" } });

        return Content(String.Format("{{'Username':'{0}'}}", username));
    }
}
