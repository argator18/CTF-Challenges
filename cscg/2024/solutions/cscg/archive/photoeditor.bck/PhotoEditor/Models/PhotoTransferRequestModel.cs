namespace PhotoEditor.Models;

public class PhotoTransferRequestModel
{
    public string Base64Blob { get; set; }

    public string DynamicAction { get; set; }
    public string Parameters { get; set; }
    public string[]? Types { get; set; }
}
