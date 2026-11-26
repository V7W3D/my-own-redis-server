using System.Net.Sockets;
using System.Net;

TcpListener? server = null;
try
{
    server = new TcpListener(IPAddress.Loopback, 6879);
    server.Start();
    TcpClient client = await server.AcceptTcpClientAsync();
    Console.WriteLine("Client successfully connected!");
}
catch (SocketException e)
{
    Console.WriteLine("SocketException: {0}", e);
}
finally
{
    server?.Stop();
}
