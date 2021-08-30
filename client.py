import socket, json, argparse

CRLF = '\r\n'
SP = ' '
CR = '\r'
HOST = '127.0.0.1'
PORT = 5000
PATH = '/'

parser = argparse.ArgumentParser(description='Client program HTTP request example.')
parser.add_argument("host", help="Server ip and port.")
parser.add_argument("opt", help="Analysis option, [0] for IXP and [1] for network per IXP.")

args = parser.parse_args()


def request_header(host=HOST, path=PATH):

  return CRLF.join([
      "GET {} HTTP/1.1".format(path), "Host: {}".format(host),
      "Connection: Close\r\n\r\n"
  ])


def parse_header(header):
  header_fields = header.split(CR)

  code = header_fields.pop(0).split(' ')[1]
  header = {}
  for field in header_fields:
      key, value = field.split(':', 1)
      header[key.lower()] = value
  return header, code


def send_request(host=HOST, path=PATH, port=PORT):
  sock = socket.socket()
  # Connect to the server.
  sock.connect((host, port))
  # Send the request.
  # print(str.encode(request_header(host, path)))
  sock.send(str.encode(request_header(host, path)))

  # Get the response.
  response = ''
  chuncks = sock.recv(4096)
  while chuncks:
      response += chuncks.decode()
      chuncks = sock.recv(4096)

  # HTTP headers will be separated from the body by an empty line
  header, _, body = response.partition(CRLF + CRLF)
  header, code = parse_header(header)
  return header, code, body


if __name__ == "__main__":

  config = args.host.split(':')
  host_ = config[0]
  port_ = int(config[1])
  # method = args.opt

  while True:
    method = input("Type your method and path: ")
    method = method.split(' ')

    if method[0] == "GET":
      header, code, body  = send_request(host=host_, port=port_, path=f'{method[1]}')
      # header, code, body2 = send_request(host=host_, port=port_, path=f'/api/netname/{1}')
      # body2 = json.loads(body2)
      body = json.loads(body)['data']['data']

      for ix in body:
        header, code, body2  = send_request(host=host_, port=port_, path=f'/api/ixnets/{ix["id"]}')
        body2 = json.loads(body2)['data']
        
        print(f"{ix['id']}\t{ix['name']}\t{len(body2)}")

      # print(f"{1} {body2['data'][0]} {body['len']}")

