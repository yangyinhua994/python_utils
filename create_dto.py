import base

java_name = base.get_file_name() + "Dto"


def build_fields_str(field: str, field_type: str, comment: str, default_value: str):
    def snake_to_camel(name: str) -> str:
        parts = name.split('_')
        return parts[0] + ''.join(x.title() for x in parts[1:])

    s = ""
    if field == "id":
        default_value = ""
    else:
        if default_value is None or default_value == "":
            default_value = base.get_default_value(field)

    example_value = base.get_example_value(field_type)

    if comment is None or comment == "":
        comment = field

    if example_value == "":
        s += f'    @ApiModelProperty(value = "{comment}")\n'
    else:
        s += f'    @ApiModelProperty(value = "{comment}", example = "{example_value}")\n'
    field_name = snake_to_camel(field)
    if field_name not in base.dto_not_check_null_fields:
        s += f'    @NotNull(message = "{comment}不能为空")\n'
        field_type = base.type_database_to_java_packaging_type(field_type)
    else:
        field_type = base.type_database_to_java(field_type)
    if default_value == "":
        s += f"    private {field_type} {field_name};\n\n"
    else:
        s += f"    private {field_type} {field_name} = {default_value};\n\n"
    return s


# 生成Java实体类
def generate_java_dto_class() -> str:
    java_class = (f"package com.example.dto;\n\n"
                  f"import io.swagger.annotations.ApiModelProperty;\n"
                  f"import lombok.Data;\n\n"
                  "import javax.validation.constraints.NotNull;\n"
                  f"import java.sql.Timestamp;\n\n"
                  f"@Data\npublic class {java_name} {{\n\n")

    for field, field_type, comment in base.get_table_fields_with_comments():
        if field in base.dto_remove_fields:
            continue
        default_value = base.get_default_value(field)
        java_class += build_fields_str(field, field_type, comment, default_value)

    for add_field, add_field_type, add_comment, add_default_value in base.dto_add_fields:
        java_class += build_fields_str(add_field, add_field_type, add_comment, add_default_value)

    java_class += "    public " + java_name + "() {\n    }"
    java_class += "\n}"
    return java_class


def start():
    base.write_file(generate_java_dto_class(), base.dto_write_path + "/" + java_name + ".java")
