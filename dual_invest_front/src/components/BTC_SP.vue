<script setup>
import DataTable from "./DataTable.vue";
</script>

<template>
    <DataTable title="BTC/USDT 低买" url="ws://localhost:8000/btc/sp" price_sort_desc="true"/>
</template>