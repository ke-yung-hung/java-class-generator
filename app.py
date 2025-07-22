from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_java():
    rows = request.get_json()  # 預期是 list of dicts
    output = ""

    current_class = ""
    class_code = ""

    for row in rows:
        class_name = row.get("className")
        field_name = row.get("fieldName")
        field_type = row.get("type")
        title = row.get("title", "")
        length = row.get("length", "")
        required = row.get("required", "")
        example = row.get("example", "")

        # 換 class 時輸出上個 class
        if class_name != current_class:
            if class_code:
                output += class_code + "}\n\n"
            current_class = class_name
            class_code = f"@Data\n@SuperBuilder\n@NoArgsConstructor\n@EqualsAndHashCode\n@ToString\npublic class {class_name} implements Serializable {{\n\n"
            class_code += f"    private static final long serialVersionUID = 123456789L;\n\n"

        # 加欄位
        annotations = f'    @Schema(title="{title}", description="{title}", '
        annotations += f'nullable={"false" if required == "V" else "true"}'
        if example:
            annotations += f', example="{example}"'
        annotations += ")\n"

        if field_type == "String":
            if required == "V":
                annotations += "    @NotBlank\n"
            if length:
                annotations += f"    @Size(max = {length})\n"
        class_code += annotations
        class_code += f"    private {field_type} {field_name};\n\n"

    if class_code:
        output += class_code + "}\n"

    return jsonify({"javaCode": output})
