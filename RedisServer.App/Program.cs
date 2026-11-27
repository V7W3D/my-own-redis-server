using System.Net.Sockets;
using System.Net;
using System.Text;

const int port = 6380;
try
{
    using TcpListener server = new TcpListener(IPAddress.Loopback, port);
    server.Start();
    using TcpClient client = await server.AcceptTcpClientAsync();
    Console.WriteLine("Client successfully connected!");
    NetworkStream stream = client.GetStream();
    byte[] buffer = new byte[256];
    int count = await stream.ReadAsync(buffer);
    string data = Encoding.UTF8.GetString(buffer, 0, count);
    Console.WriteLine("Received: {0}", data);
}
catch (SocketException e)
{
    Console.Error.WriteLine("SocketException: {0}", e);
    return 1;
}
return 0;
