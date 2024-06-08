<script setup>
import DataTable from "./DataTable.vue";
</script>

<template>
    <DataTable title="ETH/USDT 低买" url="ws://localhost:8000/eth/sp" price_sort_desc="true" />
</template>