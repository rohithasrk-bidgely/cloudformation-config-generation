user_data = {
    "Fn::Base64": {
        "Fn::Join": [
            "",
            [
                "",
                {
                    "Ref": "AWS::Region"
                },
                "\n",
                "script with line breaks \n"
            ]
        ]
    }
}
