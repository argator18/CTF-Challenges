using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using PhotoEditor.Models;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Formats;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Advanced;
using Newtonsoft.Json;

namespace PhotoEditor.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DynamicPhotoEditorController : BaseAPIController
{
    private readonly ILogger<DynamicPhotoEditorController> _logger;
    private Image _cachedImage = null;

    public DynamicPhotoEditorController(ILogger<DynamicPhotoEditorController> logger)
    {
        _logger = logger;
    }


    [HttpPost]
    [Route("EditImage")]
    public IActionResult EditImage([FromBody]PhotoTransferRequestModel photoTransferRequestModel)
    {
        try {
            this._cachedImage = Image.Load(Convert.FromBase64String(photoTransferRequestModel.Base64Blob));
            _logger.LogTrace(0, "Loaded Image: {0}", this._cachedImage);

            var actionMethod = this.GetType().GetMethod(photoTransferRequestModel.DynamicAction);
            if (actionMethod == null) {
                throw new Exception("Unable to find dynamic action: " + photoTransferRequestModel.DynamicAction);
            }

            var editParams = (object[])JsonConvert.DeserializeObject<object[]>(photoTransferRequestModel.Parameters);
            if (photoTransferRequestModel.Types != null) {
                for (int i = 0; i < photoTransferRequestModel.Types.Length; i++) {
                    editParams[i] = JsonConvert.DeserializeObject(JsonConvert.SerializeObject(editParams[i]),GetTypeByName(photoTransferRequestModel.Types[i]));
                }
            }
            
            _logger.LogWarning(0, "Params: {0} Raw: {1}", editParams, photoTransferRequestModel.Parameters);

            var transformedImage = (Image)actionMethod.Invoke(this, editParams);
            
            var imageAsBase64 = ImageToBase64(transformedImage);

            var retValue = new PhotoTransferResponseModel();    
            retValue.Base64Blob = imageAsBase64;
            return Ok(retValue);
        }
        catch (Exception e) {
            var retValue = new PhotoTransferResponseModel();    
            retValue.Error = e.Message;
            return StatusCode(StatusCodes.Status500InternalServerError, retValue);
        }
    }

    private Type GetTypeByName(String name) {
        return AppDomain.CurrentDomain.GetAssemblies()
            .Reverse()
            .Select(assembly => assembly.GetType(name))
            .FirstOrDefault(t => t != null);
    }

    public String ImageToBase64(Image image) {

         using (var memoryStream = new MemoryStream())
        {
            var imageEncoder = image.Metadata.DecodedImageFormat;
            image.SaveAsPng(memoryStream);
            return Convert.ToBase64String(memoryStream.ToArray());
        }
    }

    public Image GrayscaleImage(double amount) {
        this._cachedImage.Mutate(m => m.Grayscale((float)amount));
        return this._cachedImage;
    }

    public Image BlackWhiteImage() {
        this._cachedImage.Mutate(m => m.BlackWhite());
        return this._cachedImage;
    }

    public Image RotateImage(double degrees) {
        this._cachedImage.Mutate(m => m.Rotate((float)degrees));
        return this._cachedImage;
    }

    public Image InvertImage() {
        this._cachedImage.Mutate(m => m.Invert());
        return this._cachedImage;
    }

    public Image CropImage(RectangleStruct rect) {
        this._cachedImage.Mutate(m => m.Crop(new Rectangle(rect.X, rect.Y, rect.W, rect.H)));
        return this._cachedImage;
    }
}
