package com.example.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.entity.Textures;
import com.example.mapper.TexturesMapper;
import com.example.service.TexturesServer;
import org.springframework.stereotype.Service;

@Service
public class TexturesServerImpl extends ServiceImpl<TexturesMapper, Textures> implements TexturesServer {
}
