from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_java():
    rows = request.get_json()  # 預期輸入是 List of dict
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

        # 新類別時，先結束上一個類別
        if class_name != current_class:
            if class_code:
                output += class_code + "}\n\n"
            current_class = class_name
            class_code = (
                f"@Data\n@SuperBuilder\n@NoArgsConstructor\n@EqualsAndHashCode\n@ToString\n"
                f"public class {class_name} implements Serializable {{\n\n"
            )
            class_code += "    private static final long serialVersionUID = 123456789L;\n\n"

        # 產生欄位註解
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

if __name__ == "__main__":
    print("Running app on port", os.environ.get("PORT", 10000))
    port = int(os.environ.get("PORT", 10000))  # Render會給PORT環境變數
    app.run(host="0.0.0.0", port=port)
