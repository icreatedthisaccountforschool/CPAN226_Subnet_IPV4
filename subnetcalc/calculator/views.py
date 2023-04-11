from django.shortcuts import render

# Create your views here.

import ipaddress
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'calculator/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subnet_mask'] = ''
        return context


def index(request):
    return render(request, 'calculator/index.html')


@csrf_exempt
def calculate_subnet(request):
    if request.method == 'POST':
        try:
            network_address = request.POST.get('network_address')
            subnet_mask_length = request.POST.get('subnet_mask_length')
            print(request.POST)
            print("network_address:", network_address)
            print("subnet_mask_length:", subnet_mask_length)
            if not subnet_mask_length.isdigit() or int(subnet_mask_length) < 1 or int(subnet_mask_length) > 32:
                raise ValueError('Invalid subnet mask length')
            network_address = ipaddress.IPv4Address(network_address)
            if not ipaddress.IPv4Network(f"{network_address}/{subnet_mask_length}").supernet_of(
                    ipaddress.IPv4Network(f"{network_address}/255.255.255.255")):
                raise ValueError('Invalid network address for the given subnet mask length')
            network = ipaddress.IPv4Network(
                (network_address, subnet_mask_length),
                strict=False
            )
            response_data = {
                'success': True,
                'network_address': str(network.network_address),
                'broadcast_address': str(network.broadcast_address),
                'subnet_mask': str(network.netmask),
                'host_bits': network.num_addresses - 2
            }
            return JsonResponse(response_data)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
            print("Exception:", str(e))
            return JsonResponse({
                'success': False,
                'error': 'Invalid input: ' + str(e)
            })

        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred: {}'.format(str(e))
            })
    else:
        return HttpResponse('Method not allowed.', status=405)



