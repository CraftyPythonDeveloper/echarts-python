from collections import defaultdict
from pyecharts import options as opts
from pyecharts.charts import Pie


def aggregate_data(data, aggregation_type: str = "Count"):
    """
    This function is used to aggregate the data. The expected format of data is
    following: [
        [
            {"value": "Sunday"}
            {"value": 5}
        ],
        [
            {"value": "Monday"}
            {"value": 10}
        ],
        [
            {"value": "Sunday"}
            {"value": 3}
        ],
        [
            {"value": "Tuesday"}
            {"value": 15}
        ],
        [
            {"value": "Tuesday"}
            {"value": 40}
        ]
    ]
    :param data: data to be aggregated
    :param aggregation_type: how the data is to be aggregated. Default value is "Count"
    :return: list of aggregated data. [("Sunday": 2), ("Monday": 1), ("Tuesday": 2)]
    """
    aggregation_type = aggregation_type.lower()
    grouped_data = defaultdict(list)

    for entry in data:
        category = entry[0]['value']
        if not category:
            continue
        value = entry[1]['value']
        grouped_data[category].append(value)

    aggregated_data = []
    for category, values in grouped_data.items():
        if aggregation_type == "count":
            aggregated_data.append((category, len(values)))
        elif aggregation_type == "sum":
            aggregated_data.append((category, sum(values)))
        elif aggregation_type == "min":
            aggregated_data.append((category, min(values)))
        elif aggregation_type == "max":
            aggregated_data.append((category, max(values)))
        else:
            raise ValueError(f"Unsupported aggregation type: {aggregation_type}")

    return aggregated_data


def aggregate_value(data: list, aggregation_type: str = "Count", value_index: int = 1):
    """
    This function takes list of values and aggregates them in one single value
    :param data: List of values.  [("Sunday": 2), ("Monday": 1), ("Tuesday": 2)]
    :param aggregation_type: how the value is to be aggregated. Default value is "Count"
    :param value_index: index of the value to be aggregated. Default value is 1
    :return: int
    """
    aggregation_type = aggregation_type.lower()
    data = [i[value_index] for i in data]
    if aggregation_type == "count":
        return len(data)
    elif aggregation_type == "sum":
        return sum(data)
    elif aggregation_type == "min":
        return min(data)
    elif aggregation_type == "max":
        return max(data)
    else:
        raise ValueError(f"Unsupported aggregation type: {aggregation_type}")


def create_pie(config, output_format: str = "code"):
    """
    Create a pie chart
    :param config: the config to create the pie chart
    :param output_format: how the output should be, default value is return code. Supported values are "html" and "code"
    :return: html code or path
    """
    agg_type = config['measures']['agrType']
    data = aggregate_data(data=config["data"], aggregation_type=agg_type)
    data_value = aggregate_value(data=data, aggregation_type=agg_type)

    chart = (
        Pie(init_opts=opts.InitOpts(width=f"{config['width']}px", height=f"{config['height']}px"))
        .add(
            series_name=config['title'],
            data_pair=data,
            radius=[f"{config['outerRadius']}%", "70%"],
            label_opts=opts.LabelOpts(is_show=True)
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(pos_bottom="5%"),
            title_opts=opts.TitleOpts(
                title=config['title'],
                subtitle=f"{config['subTitle']} {agg_type}: {data_value}",
                title_textstyle_opts=opts.TextStyleOpts(font_size=config['chartTitleFsz']),
                subtitle_textstyle_opts=opts.TextStyleOpts(font_size=config['subTitleFsz']),
                pos_left=config['chartTitlePosition']
            )
        )
    )

    if output_format == "html":
        filename = config['title'] + ".html"
        return chart.render(filename)

    return chart.render_embed()

