using System.Net.Sockets;
using System.Net;

const int Port = 6380;
try
{
    using TcpListener server = new TcpListener(IPAddress.Loopback, Port);
    server.Start();
    using TcpClient client = await server.AcceptTcpClientAsync();
    Console.WriteLine("Client successfully connected!");
}
catch (SocketException e)
{
    Console.Error.WriteLine("SocketException: {0}", e);
    return 1;
}
return 0;
