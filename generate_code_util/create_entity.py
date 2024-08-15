import base

java_name = base.get_file_name_last_upper()


def build_fields_str(field: str, field_type: str, comment: str, default_value: str):
    def snake_to_camel(name: str) -> str:
        parts = name.split('_')
        return parts[0] + ''.join(x.title() for x in parts[1:])

    s = ""
    # if default_value is None or default_value == "":
    #     default_value = base.get_default_value(field)

    if comment is None or comment == "":
        comment = field

    s += f"    /**\n     * {comment}\n     */\n"
    # if default_value is None or default_value == "":
    #     s += f"    private {base.type_database_to_java(field_type)} {snake_to_camel(field)};\n\n"
    # else:
    #     s += f"    private {base.type_database_to_java(field_type)} {snake_to_camel(field)} = {default_value};\n\n"
    s += f"    private {base.type_database_to_java(field_type)} {snake_to_camel(field)};\n\n"
    return s


# 生成Java实体类
def generate_java_entity_class() -> str:
    java_class = (f"package com.example.entity;\n\n"
                  f"import com.baomidou.mybatisplus.annotation.TableName;\n"
                  f"import lombok.Data;\n"
                  f"import lombok.EqualsAndHashCode;\n\n"
                  "/**\n"
                  " * @author yyh\n"
                  " */\n"
                  "@EqualsAndHashCode(callSuper = true)\n"
                  f"@Data\n"
                  f'@TableName("{base.database_table_name}")\n'
                  f"public class {java_name} extends BaseEntity {{\n\n")

    for field, field_type, comment in base.get_table_fields_with_comments():
        if field in base.entity_remove_fields:
            continue
        default_value = base.get_default_value(field)
        java_class += build_fields_str(field, field_type, comment, default_value)
    for add_field, add_field_type, add_comment, add_default_value in base.entity_add_fields:
        java_class += build_fields_str(add_field, add_field_type, add_comment, add_default_value)

    java_class += "    public " + java_name + "() {\n    }"
    java_class += "\n}"
    return java_class


def start():
    base.write_file(generate_java_entity_class(), base.entity_write_path + "/" + java_name + ".java")
