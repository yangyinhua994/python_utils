package com.example.controller;

import com.example.dto.TexturesDto;
import com.example.entity.Textures;
import com.example.enumeration.BaseStateEnum;
import com.example.msg.MsgEnum;
import com.example.respone.Result;
import com.example.service.TexturesServer;
import com.example.utils.CheckUtil;
import com.example.utils.EntityUtil;
import com.example.utils.TimeUtil;
import com.example.vo.TexturesVo;
import io.swagger.annotations.ApiOperation;
import org.springframework.validation.BindingResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.sql.Timestamp;
import java.util.Objects;

@RestController
@RequestMapping("/textures")
@Validated
public class TexturesController {

    private final TexturesServer texturesServer;

    public TexturesController(TexturesServer texturesServer) {
        this.texturesServer = texturesServer;
    }

    @ApiOperation("新增数据")
    @PostMapping("/add")
    public Result<TexturesVo> add(@Valid @RequestBody TexturesDto texturesDto, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return Result.fail(Objects.requireNonNull(bindingResult.getFieldError()).getDefaultMessage());
        }
        Textures convert = EntityUtil.convert(texturesDto, Textures.class);
        Timestamp now = TimeUtil.now();
        convert.setCreateTime(now);
        convert.setUpdateTime(now);
        convert.setStatus(BaseStateEnum.DELETE_STATE_ENABLE.getState());
        return (texturesServer.save(convert) ? Result.success() : Result.fail());
    }

    @ApiOperation("根据id更新数据")
    @PatchMapping("/updateById")
    public Result<TexturesVo> updateById(@RequestBody TexturesDto texturesDto, BindingResult bindingResult) {
        CheckUtil.checkEmpty(texturesDto.getId(), "id");
        if (bindingResult.hasErrors()) {
            return Result.fail(Objects.requireNonNull(bindingResult.getFieldError()).getDefaultMessage());
        }
        if (texturesServer.getById(texturesDto.getId()) == null) {
            return Result.fail(MsgEnum.ID_NOT_EXIST);
        }
        Textures convert = EntityUtil.convert(texturesDto, Textures.class);
        convert.setUpdateTime(TimeUtil.now());
        return (texturesServer.updateById(convert)) ? Result.success() : Result.fail();
    }

    @ApiOperation("根据id删除数据")
    @DeleteMapping("/deleteById")
    public Result<TexturesVo> deleteById(Long id) {
        CheckUtil.checkEmpty(id, "id");
        if (texturesServer.getById(id) == null) {
            return Result.fail(MsgEnum.ID_NOT_EXIST);
        }
        return (texturesServer.removeById(id)) ? Result.success() : Result.fail();
    }

    @ApiOperation("根据id获取数据")
    @GetMapping("/getById")
    public Result<TexturesVo> getById(Long id) {
        CheckUtil.checkEmpty(id, "id");
        Textures textures = texturesServer.getById(id);
        return CheckUtil.isEmpty(texturesServer.getById(id)) ? Result.fail(MsgEnum.ID_NOT_EXIST) : Result.success(EntityUtil.convert(textures, TexturesVo.class));
    }

}
