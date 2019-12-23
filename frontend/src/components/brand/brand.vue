<template>
  <div class="content-wrap">
    <div class="handle-box">
      <el-button
        type="primary"
        icon="el-icon-plus"
        class="handle-del mr10"
        @click="handleAdd"
      >新增</el-button>
      <el-input
        v-model="searchInfo"
        placeholder="请输入品牌名称"
        class="handle-input mr10"
      ></el-input>
      <el-button
        @click="search"
        type="primary"
        icon="el-icon-search"
      >查询</el-button>
    </div>
    <el-table
      v-loading="loading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="#fff"
      border
      :data="tableData"
      :row-style="{height:'10px'}"
      class="table">
      <el-table-column type="index" label="序号" width="50" show-overflow-tooltip align="center"></el-table-column>
      <el-table-column prop="brandName" min-width="160" label="品牌名称" show-overflow-tooltip align="center"></el-table-column>
      <el-table-column prop="busFormatName" min-width="160" label="所属业态" show-overflow-tooltip align="center"></el-table-column>
      <el-table-column prop="operatorName" min-width="150" label="更新人" show-overflow-tooltip align="center"></el-table-column>
      <el-table-column prop="operatorTime" min-width="200" label="更新时间" show-overflow-tooltip align="center">
        <template v-slot="scope">
          <span>{{scope.row.operatorTime | getDate}}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="200" align="center">
        <template v-slot="scope">
          <el-button
            type="text"
            icon="el-icon-edit"
            class="mr10"
            @click="handleEdit(scope.row)"
          >编辑</el-button>
          <el-popover
            width="160"
            v-model="scope.row.visible">
            <div class="text_center">确定删除吗？</div>
            <div class="text_center mt20">
              <el-button size="mini" @click="scope.row.visible = false">取消</el-button>
              <el-button type="primary" size="mini" @click="handelDel(scope.row)">确定</el-button>
            </div>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              slot="reference"
            >删除</el-button>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
    <div class="text_center mt20">
      <el-pagination
        background
        layout="prev, pager, next,jumper,sizes"
        :page-sizes="[10, 50, 100, 200]"
        :page-size="pageSize"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :total="total"
      ></el-pagination>
    </div>
    <el-dialog
      :title="`品牌${flag?'编辑':'新增'}`"
      :visible.sync="editVisible"
      width="360px"
      @closed="cancelEdit"
    >
      <el-form :model="form" ref="brandForm" :rules="rules" label-width="90px">
        <el-form-item
          label="品牌名称"
          prop="brandName"
        >
          <el-input style="width:200px" v-model="form.brandName" placeholder="请输入品牌名称"></el-input>
        </el-form-item>
        <el-form-item
          label="所属业态"
          prop="busFormatId"
          :rules="{
            required: true, message: '业态不能为空', trigger: 'blur'
          }"
        >
          <el-select v-model="form.busFormatId"
            placeholder="请选择业态"
            class="mr10"
          >
            <el-option v-for="item in businessFormat" :key="item.id" :label="item.busFormatName" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div class="text_center">
        <el-button @click="editVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveEdit(form)">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
// import { getBrand, updateBrand, addBrand, delBrand, getBusinessFormat } from '@/api/request'
// import { getDate } from '@/libs/tools'
export default {
  data () {
    return {
      tableData: [], // 表格数据
      editVisible: false, // 显示隐藏模态框
      form: {
        brandCode: '',
        brandName: '',
        busFormatId: '',
        id: 0
      }, // 模态框数据
      loading: false,
      formCopy: {}, // 缓存表格中的数据用于比较是否修改
      flag: true, // true编辑，false新增
      searchInfo: '', // 搜索信息
      searchs: '', // 确定的搜索信息
      currentPage: 1,
      pageSize: 10,
      total: 0,
      businessFormat: [],
      rules: {
        brandName: [
          { required: true, message: '品牌名称不能为空', trigger: 'blur' },
          { max: 30, message: '最多可输入30个字符', trigger: 'blur' }
        ],
        busFormatId: [
          { required: true, message: '业态不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {

  },
  created () {
    this.loading = true
    getBrand().then(res => {
      this.loading = false
      this.total = res.data.total
      this.tableData = res.data.records
    })
  },
  filters: {
    getDate (val) {
      return getDate(val)
    }
  },
  methods: {
    // 提交品牌类型
    _getData () {
      this.loading = true
      getBrand({ pageNum: this.currentPage, brandName: this.searchs, pageSize: this.pageSize }).then(res => {
        this.loading = false
        this.total = res.data.total
        this.tableData = res.data.records
        console.log(this.tableData)
      })
    },
    saveEdit (form) {
      // 判断是增加还是修改数据
      if (this.flag) {
        // 判断信息是否有修改
        if (this.formCopy.brandName === this.form.brandName && this.formCopy.busFormatId === this.form.busFormatId) {
          this.editVisible = false
          // console.log("数据未修改")
        } else {
          this.$refs.brandForm.validate((valid) => {
            if (valid) {
              this.editVisible = false
              updateBrand(form).then(res => {
                this._getData()
              })
            } else {
              return false
            }
          })
        }
      } else {
        this.$refs.brandForm.validate((valid) => {
          if (valid) {
            this.editVisible = false
            addBrand(form).then(res => {
              this._getData()
            })
          } else {
            return false
          }
        })
      }
    },
    cancelEdit () {
      this.$refs.brandForm.clearValidate()
    },
    // 编辑品牌类型
    handleEdit (row) {
      this.loadBusinessFormat()
      this.flag = true
      this.form = JSON.parse(JSON.stringify(row))
      this.formCopy = JSON.parse(JSON.stringify(row))
      this.editVisible = true
    },
    // 新增品牌类型
    handleAdd () {
      this.loadBusinessFormat()
      this.flag = false
      this.form = {}
      this.editVisible = true
    },
    // 修改为删除接口
    handelDel (row) {
      row.visible = false
      delBrand(row).then(res => {
        this._getData()
      })
    },
    // 查询品牌信息，添加接口
    search () {
      this.currentPage = 1
      this.searchs = this.searchInfo
      this._getData()
    },
    handleSizeChange (val) {
      this.currentPage = 1
      this.pageSize = val
      this._getData()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this._getData()
    },
    loadBusinessFormat () {
      if (!this.businessFormat.length) {
        getBusinessFormat({pageSize:99999}).then(res => {
          this.businessFormat = res.data.records
        })
      } else {
        console.log('已有数据')
      }
    }
  }
}
</script>

<style lang="less" scoped>

</style>
