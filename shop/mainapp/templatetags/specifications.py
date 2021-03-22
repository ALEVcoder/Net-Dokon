from django import template
from django.utils.safestring import mark_safe

register = template.Library()



TABLE_HEAD = """
			
				<table class="table">
					<tbody>

			 """

TABLE_TAIL = """
					</tbody>
				</table>
			 """
TABLE_CONTENT = """
				<tr>
					<td>{name}</td>
					<td>{value}</td>
				</tr>
				"""

PRODUCT_SPEC = {
	'notebook': {
		'Diagonal': 'diagonal',
		'Tip Displaya': 'display_type',
		'Chastota Protsesora': 'processor_freq',
		'Operativnaya Pamyat': 'ram',
		'Video Karta': 'video',
		'Akumlyatora': 'time_without_charge'
	},
	'smartphone': {
		'Diagonal': 'diagonal',
		'Tip Displaya': 'display_type',
		'Razreshena ekrana': 'resolution',
		'Zaryad acumlyatora': 'accum_volume',
		'Operativnaya pamyot': 'ram',
		'CD karti': 'sd',
		'Maksimalnaya CD karti': 'sd_volume_max',
		'Glavniya Camera': 'main_cam_mp',
		'Frontal camera': 'frontal_cam_mp',
	}
}


def get_product_spec(product, model_name):
	table_content = ''
	for name, value in PRODUCT_SPEC[model_name].items():
		table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
	return table_content




@register.filter
def product_spec(product, arg):
	print(arg, 'arg_value')
	model_name = product.__class__._meta.model_name
	return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)