import base

java_name = base.get_file_name_last_upper() + "Vo"


def build_fields_str(field: str, field_type: str, comment: str):
    def snake_to_camel(name: str) -> str:
        parts = name.split('_')
        return parts[0] + ''.join(x.title() for x in parts[1:])

    s = ""
    if comment is None or comment == "":
        comment = field
    s += f"    /**\n     * {comment}\n     */\n"
    s += f"    private {base.type_database_to_java(field_type)} {snake_to_camel(field)};\n\n"
    return s


# 生成Java实体类
def generate_java_vo_class() -> str:
    java_class = (f"package com.example.vo;\n\n"
                  f"import lombok.Data;\n\n"
                  f"@Data\npublic class {java_name} {{\n\n")

    for field, field_type, comment in base.get_table_fields_with_comments():
        if field in base.vo_remove_fields:
            continue
        java_class += build_fields_str(field, field_type, comment)
    for add_field, add_field_type, add_comment, add_default_value in base.vo_add_fields:
        java_class += build_fields_str(add_field, add_field_type, add_comment)

    java_class += "    public " + java_name + "() {\n    }"
    java_class += "\n}"
    return java_class


def start():
    base.write_file(generate_java_vo_class(), base.vo_write_path + "/" + java_name + ".java")
