using System.Text;

namespace RedisServer.App;

public static class DebugText
{
    public static string EscapeControlChars(string data)
    {
        StringBuilder escapedData = new StringBuilder(data.Length);
        foreach (char c in data)
        {
            if(c == '\n') escapedData.Append("\\n");
            else if(c == '\r') escapedData.Append("\\r");
            else escapedData.Append(c);
        }
        return escapedData.ToString();
    } 
}