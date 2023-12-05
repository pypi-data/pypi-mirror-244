
public class {{ table_name }} {

    {% for column in columns %}
         /**
        * {{ column.comment}}
        */
         private {{column.javatype}} {{column.name}};
    {% endfor %}
    
}