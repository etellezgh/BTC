{% macro convert_to_usd(column_name) %}

{{column_name}} * (
     select 
        close_price_usd
    from {{ ref('btc_usd_max')}}
        where try_to_date(replace(event_date,' UTC','')) <= current_date()
        qualify row_number() over (
            order by try_to_date(replace(event_date,' UTC','')) desc
        ) = 1
)

{% endmacro %}