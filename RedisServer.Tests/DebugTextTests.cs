using RedisServer.App;

namespace RedisServer.Tests;

public class DebugTextTests
{
    [Fact]
    public void EscapeControlChars_EmptyString_ReturnsEmptyString()
    {
        Assert.Equal("", DebugText.EscapeControlChars(""));
    }

    [Theory]
    [InlineData("PING")]
    [InlineData("hello world")]
    [InlineData("*1$4")]
    public void EscapeControlChars_NoControlChars_ReturnsInputUnchanged(string input)
    {
        Assert.Equal(input, DebugText.EscapeControlChars(input));
    }

    [Theory]
    [InlineData("\n", "\\n")]
    [InlineData("\r", "\\r")]
    [InlineData("\r\n", "\\r\\n")]
    [InlineData("\n\n", "\\n\\n")]
    public void EscapeControlChars_OnlyControlChars_EscapesEach(string input, string expected)
    {
        Assert.Equal(expected, DebugText.EscapeControlChars(input));
    }

    [Fact]
    public void EscapeControlChars_RespCommand_EscapesCrlfSeparators()
    {
        string input = "*1\r\n$4\r\nPING\r\n";

        string result = DebugText.EscapeControlChars(input);

        Assert.Equal("*1\\r\\n$4\\r\\nPING\\r\\n", result);
    }

    [Fact]
    public void EscapeControlChars_Result_ContainsNoRawCrOrLf()
    {
        string result = DebugText.EscapeControlChars("a\rb\nc\r\nd");

        Assert.DoesNotContain('\r', result);
        Assert.DoesNotContain('\n', result);
    }

    [Theory]
    [InlineData("\t")]
    [InlineData("\0")]
    [InlineData("\\n")]
    public void EscapeControlChars_OtherCharacters_AreLeftAsIs(string input)
    {
        Assert.Equal(input, DebugText.EscapeControlChars(input));
    }
}
