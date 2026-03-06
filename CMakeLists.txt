idf_build_get_property(target IDF_TARGET)

if(${target} STREQUAL "linux")
    return()
endif()

set(IDF_BT_COMPONENT_DIR "$ENV{IDF_PATH}/components/bt")
if(NOT EXISTS "${IDF_BT_COMPONENT_DIR}/CMakeLists.txt")
    message(FATAL_ERROR "ESP-IDF BT component not found at ${IDF_BT_COMPONENT_DIR}")
endif()

if(CONFIG_IDF_TARGET_ESP32S3)
    set(target_name "esp32c3")
elseif(CONFIG_IDF_TARGET_ESP32C61)
    set(target_name "esp32c6")
else()
    set(target_name "${idf_target}")
endif()

if(CONFIG_BT_ENABLED)
    set(srcs "")
    set(include_dirs "")
    set(priv_include_dirs "")
    set(ldscripts "${IDF_BT_COMPONENT_DIR}/linker_common.lf")

    if(CONFIG_BT_CONTROLLER_ENABLED)
        list(APPEND include_dirs "${IDF_BT_COMPONENT_DIR}/include/${target_name}/include")

        if(CONFIG_IDF_TARGET_ESP32)
            list(APPEND srcs
                "${IDF_BT_COMPONENT_DIR}/controller/esp32/bt.c"
                "${IDF_BT_COMPONENT_DIR}/controller/esp32/hli_api.c"
                "${IDF_BT_COMPONENT_DIR}/controller/esp32/hli_vectors.S"
            )
            list(APPEND ldscripts "${IDF_BT_COMPONENT_DIR}/linker_rw_bt_controller.lf")
        elseif(CONFIG_IDF_TARGET_ESP32C3 OR CONFIG_IDF_TARGET_ESP32S3)
            list(APPEND srcs "${IDF_BT_COMPONENT_DIR}/controller/${target_name}/bt.c")
            list(APPEND ldscripts "${IDF_BT_COMPONENT_DIR}/linker_rw_bt_controller.lf")
        elseif(CONFIG_IDF_TARGET_ESP32C2)
            list(APPEND srcs
                "${IDF_BT_COMPONENT_DIR}/controller/esp32c2/bt.c"
                "${IDF_BT_COMPONENT_DIR}/controller/esp32c2/ble.c"
            )
            if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
                list(APPEND srcs "${IDF_BT_COMPONENT_DIR}/controller/esp32c2/dummy.c")
            endif()
            list(APPEND ldscripts "${IDF_BT_COMPONENT_DIR}/linker_esp32c2.lf")
        else()
            list(APPEND srcs
                "${IDF_BT_COMPONENT_DIR}/controller/${target_name}/bt.c"
                "${IDF_BT_COMPONENT_DIR}/controller/${target_name}/ble.c"
            )
            list(APPEND ldscripts "${IDF_BT_COMPONENT_DIR}/linker_esp_ble_controller.lf")
        endif()
    endif()

    list(APPEND include_dirs
        "${IDF_BT_COMPONENT_DIR}/common/osi/include"
        "${IDF_BT_COMPONENT_DIR}/common/api/include/api"
        "${IDF_BT_COMPONENT_DIR}/common/btc/profile/esp/blufi/include"
        "${IDF_BT_COMPONENT_DIR}/common/btc/profile/esp/include"
        "${IDF_BT_COMPONENT_DIR}/common/hci_log/include"
        "${IDF_BT_COMPONENT_DIR}/common/ble_log/include"
        "$ENV{IDF_PATH}/components/esp_wifi/include"
        "$ENV{IDF_PATH}/components/esp_timer/include"
        "$ENV{IDF_PATH}/components/esp_phy/include"
        "$ENV{IDF_PATH}/components/esp_event/include"
        "$ENV{IDF_PATH}/components/esp_netif/include"
        "$ENV{IDF_PATH}/components/esp_pm/include"
        "$ENV{IDF_PATH}/components/esp_coex/include"
        "$ENV{IDF_PATH}/components/nvs_flash/include"
        "$ENV{IDF_PATH}/components/esp_partition/include"
        "$ENV{IDF_PATH}/components/mbedtls/mbedtls/include"
        "$ENV{IDF_PATH}/components/mbedtls/port/include"
        "$ENV{IDF_PATH}/components/esp_driver_uart/include"
        "$ENV{IDF_PATH}/components/vfs/include"
        "$ENV{IDF_PATH}/components/esp_ringbuf/include"
        "$ENV{IDF_PATH}/components/esp_driver_spi/include"
        "$ENV{IDF_PATH}/components/esp_driver_gpio/include"
    )

    list(APPEND priv_include_dirs
        "${IDF_BT_COMPONENT_DIR}/common/btc/include"
        "${IDF_BT_COMPONENT_DIR}/common/include"
        "${IDF_BT_COMPONENT_DIR}/porting/mem"
        "${IDF_BT_COMPONENT_DIR}/porting/include"
    )

    list(APPEND srcs
        "${IDF_BT_COMPONENT_DIR}/common/btc/core/btc_alarm.c"
        "${IDF_BT_COMPONENT_DIR}/common/api/esp_blufi_api.c"
        "${IDF_BT_COMPONENT_DIR}/common/hci_log/bt_hci_log.c"
        "${IDF_BT_COMPONENT_DIR}/common/btc/core/btc_manage.c"
        "${IDF_BT_COMPONENT_DIR}/common/btc/core/btc_task.c"
        "${IDF_BT_COMPONENT_DIR}/common/btc/profile/esp/blufi/blufi_prf.c"
        "${IDF_BT_COMPONENT_DIR}/common/btc/profile/esp/blufi/blufi_protocol.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/alarm.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/allocator.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/buffer.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/config.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/fixed_queue.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/pkt_queue.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/fixed_pkt_queue.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/future.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/hash_functions.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/hash_map.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/list.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/mutex.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/thread.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/osi.c"
        "${IDF_BT_COMPONENT_DIR}/common/osi/semaphore.c"
        "${IDF_BT_COMPONENT_DIR}/porting/mem/bt_osi_mem.c"
        "${IDF_BT_COMPONENT_DIR}/common/ble_log/ble_log_spi_out.c"
    )

    if(CONFIG_BT_NIMBLE_ENABLED)
        set(NIMBLE_ROOT "${CMAKE_CURRENT_LIST_DIR}/host/nimble")

        set(nimble_include_dirs
            "${NIMBLE_ROOT}/nimble/nimble/host/include"
            "${NIMBLE_ROOT}/nimble/nimble/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ans/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/bas/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/dis/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/gap/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/gatt/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/hr/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/htp/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ias/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ipss/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/lls/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/prox/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/cts/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/tps/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/hid/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/sps/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/cte/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/util/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/ram/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/include"
            "${NIMBLE_ROOT}/nimble/porting/nimble/include"
            "${NIMBLE_ROOT}/port/include"
            "${NIMBLE_ROOT}/nimble/nimble/transport/include"
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/include"
            "${NIMBLE_ROOT}/esp-hci/include"
            "${IDF_BT_COMPONENT_DIR}/porting/include"
        )
        list(APPEND include_dirs ${nimble_include_dirs})

        file(GLOB nimble_host_srcs "${NIMBLE_ROOT}/nimble/nimble/host/src/*.c")
        file(GLOB nimble_services_srcs "${NIMBLE_ROOT}/nimble/nimble/host/services/*/src/*.c")
        list(FILTER nimble_host_srcs EXCLUDE REGEX ".*/ble_sm_alg\\.c$")
        list(FILTER nimble_host_srcs EXCLUDE REGEX ".*/ble_aes_ccm\\.c$")
        list(FILTER nimble_services_srcs EXCLUDE REGEX ".*/services/bleuart/.*")

        set(nimble_crypto_srcs
            "${NIMBLE_ROOT}/nimble/nimble/host/src/ble_sm_alg.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/src/ble_aes_ccm.c"
        )

        if(NOT (CONFIG_BT_LE_CRYPTO_STACK_MBEDTLS OR CONFIG_BT_NIMBLE_CRYPTO_STACK_MBEDTLS))
            list(APPEND include_dirs "${NIMBLE_ROOT}/nimble/ext/tinycrypt/include")
            file(GLOB nimble_tinycrypt_srcs "${NIMBLE_ROOT}/nimble/ext/tinycrypt/src/*.c")
            list(APPEND nimble_crypto_srcs ${nimble_tinycrypt_srcs})
        endif()

        list(APPEND srcs
            "${NIMBLE_ROOT}/nimble/nimble/transport/src/transport.c"
            ${nimble_host_srcs}
            ${nimble_services_srcs}
            "${NIMBLE_ROOT}/nimble/nimble/host/util/src/addr.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/ram/src/ble_store_ram.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/src/ble_store_config.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/src/ble_store_nvs.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/nimble_port.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/endian.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_mempool.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/mem.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_mbuf.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_msys_init.c"
            ${nimble_crypto_srcs}
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/src/nimble_port_freertos.c"
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/src/npl_os_freertos.c"
            "${NIMBLE_ROOT}/port/src/nvs_port.c"
            "${NIMBLE_ROOT}/esp-hci/src/esp_nimble_hci.c"
            "${NIMBLE_ROOT}/nimble/nimble/transport/esp_ipc_legacy/src/hci_esp_ipc_legacy.c"
            "${IDF_BT_COMPONENT_DIR}/common/btc/profile/esp/blufi/nimble_host/esp_blufi.c"
        )
    endif()

    idf_component_register(
        SRCS ${srcs}
        INCLUDE_DIRS ${include_dirs}
        PRIV_INCLUDE_DIRS ${priv_include_dirs}
        REQUIRES esp_timer esp_wifi
        PRIV_REQUIRES nvs_flash soc esp_pm esp_phy esp_coex mbedtls esp_driver_uart vfs esp_ringbuf esp_driver_spi esp_driver_gpio
        LDFRAGMENTS ${ldscripts}
    )

    if(CONFIG_IDF_TARGET_ESP32)
        set_source_files_properties("${IDF_BT_COMPONENT_DIR}/controller/esp32/hli_vectors.S" PROPERTIES COMPILE_FLAGS "-x assembler-with-cpp")
    endif()

    target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-implicit-fallthrough -Wno-unused-const-variable)
    target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
    target_compile_definitions(${COMPONENT_LIB} PRIVATE MBEDTLS_CONFIG_FILE="mbedtls/esp_config.h")

    if(CONFIG_IDF_TARGET_ESP32)
        target_link_directories(${COMPONENT_LIB} INTERFACE "${IDF_BT_COMPONENT_DIR}/controller/lib_esp32/esp32")
        target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app)
        target_link_libraries(${COMPONENT_LIB} INTERFACE "-u ld_include_hli_vectors_bt")
    elseif(CONFIG_IDF_TARGET_ESP32C3)
        target_link_directories(${COMPONENT_LIB} INTERFACE "${IDF_BT_COMPONENT_DIR}/controller/lib_esp32c3_family/esp32c3")
        if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
            target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app_flash)
        else()
            target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app)
        endif()
    elseif(CONFIG_IDF_TARGET_ESP32S3)
        target_link_directories(${COMPONENT_LIB} INTERFACE "${IDF_BT_COMPONENT_DIR}/controller/lib_esp32c3_family/esp32s3")
        if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
            target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app_flash)
        else()
            target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app)
        endif()
    elseif(CONFIG_BT_CONTROLLER_ENABLED)
        if(CONFIG_BT_LE_CONTROLLER_LOG_WRAP_PANIC_HANDLER_ENABLE)
            target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=esp_panic_handler")
        endif()

        if(CONFIG_IDF_TARGET_ESP32C6)
            add_prebuilt_library(libble_app
                "${IDF_BT_COMPONENT_DIR}/controller/lib_esp32c6/esp32c6-bt-lib/esp32c6/libble_app.a")
        elseif(CONFIG_IDF_TARGET_ESP32C61)
            add_prebuilt_library(libble_app
                "${IDF_BT_COMPONENT_DIR}/controller/lib_esp32c6/esp32c6-bt-lib/esp32c61/libble_app.a")
        else()
            if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY AND CONFIG_IDF_TARGET_ESP32C2)
                add_prebuilt_library(libble_app
                    "${IDF_BT_COMPONENT_DIR}/controller/lib_${target_name}/${target_name}-bt-lib/libble_app_flash.a")
            else()
                add_prebuilt_library(libble_app
                    "${IDF_BT_COMPONENT_DIR}/controller/lib_${target_name}/${target_name}-bt-lib/libble_app.a")
            endif()
        endif()

        target_link_libraries(${COMPONENT_LIB} PRIVATE libble_app)
    endif()
else()
    idf_component_register()
endif()
