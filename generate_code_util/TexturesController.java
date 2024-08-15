package com.example.controller;

import io.swagger.annotations.Api;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author yyh
 */
@Api(tags = "贴图管理接口")
@RestController
@RequestMapping("/textures")
@Validated
public class TexturesController {

}
